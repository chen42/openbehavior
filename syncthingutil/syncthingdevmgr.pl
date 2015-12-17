#!/usr/bin/perl

# Copyright 2015 University of Tennessee Health Sciences Center
# Author: Matthew Longley <mlongle1@uthsc.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

use strict; use warnings;
use XML::LibXML;

# Path to configuration file on Linux
my $configfile = '/home/' . $ENV{LOGNAME} . '/.config/syncthing/config.xml';

# Subroutine to print this device's ID
sub ThisDeviceID {
    my $doc = $_[0];
    my ($device) = ($doc->findnodes('/configuration/folder/device'));
    print $device->getAttribute('id'), "\n";
}

# Subroutine to match device IDs used for Syncthing
sub ValidateDeviceID {
    my $id = $_[0];
    if($id =~ /[A-Z0-9]{7}-[A-Z0-9]{7}-[A-Z0-9]{7}-[A-Z0-9]{7}-[A-Z0-9]{7}-[A-Z0-9]{7}-[A-Z0-9]{7}-[A-Z0-9]{7}/) {
	return 1;
    } else {
	return 0;
    }
}
   
# Subroutine to print all device IDs currently registered
sub PrintRegisteredDevices {
    my $doc = $_[0];
    foreach my $device ($doc->findnodes('/configuration/device')) {
	my($deviceid) = $device->getAttribute('id');
	my($devicename) = $device->getAttribute('name');
	print $devicename, " -> ", $deviceid, "\n";
    }
}

# Subroutine to display how to use tool
sub PrintUsage {
    print STDERR "Usage: ", $0, " <ACTION> {<DEVICE ID>}\n";
    print STDERR "Where ACTION is one of:\n";
    print STDERR "\tlist - list all registered devices\n";
    print STDERR "\tthis - show this device's id\n";
    print STDERR "\tadd - add a device\n";
    print STDERR "\tremove - remove a device\n";
}

# Subroutine to generate a new device node
sub GenDeviceNode {
    # Device ID arg
    my $id = $_[0];
    # Create new node
    my $node = XML::LibXML::Element->new('device');
    $node->setAttribute('id', $id);
    $node->setAttribute('name', '');
    $node->setAttribute('compression', 'metadata');
    $node->setAttribute('introducer', 'false');
    # Create child node for new node
    my $childnode = XML::LibXML::Element->new('address');
    $childnode->appendText('dynamic');
    # Add child node to parent
    $node->addChild($childnode);
    # Return new node
    return $node;
}

# Subroutine to add a device ID
sub AddDeviceID {
    my $id = $_[0];
    my $doc = $_[1];
    # verify that id is valid
    if(&ValidateDeviceID($id)) {
	my ($configuration) = $doc->findnodes('/configuration');
	my $newnode = &GenDeviceNode($id);
	$configuration->addChild($newnode);
    } else {
	&PrintUsage();
	print STDERR "ERROR: invalid device id\n";
    }
}

# Subroutine to remove a device ID
sub RemDeviceID {
    my $id = $_[0];
    my $doc = $_[1];
    # verify that id is valid
    if(&ValidateDeviceID($id)) {
	foreach my $device($doc->findnodes('/configuration/device')) {
	    if($device->getAttribute('id') eq $id) {
		my $configuration = $device->parentNode;
		$configuration->removeChild($device);
	    }
	}
	foreach my $folderdev($doc->findnodes('/configuration/folder/device')) {
	    if($folderdev->getAttribute('id') eq $id) {
		my $folder = $folderdev->parentNode;
		$folder->removeChild($folderdev);
	    }
	}
    } else {
	&PrintUsage();
	print STDERR "ERROR: invalid device id\n";
    }
}

# Subroutine to share all folders to connected devices
sub ShareFoldersToAll {
    my $doc = $_[0];
    # Get all connected device IDs
    my @devices = $doc->findnodes('/configuration/device');
    # Add each device to each folder
    foreach my $folder($doc->findnodes('/configuration/folder')) {
	foreach my $device(@devices) {
	    # Create the device node
	    my $devnode = XML::LibXML::Element->new('device');
	    $devnode->setAttribute('id', $device->getAttribute('id'));
	    # Attach it to the folder
	    $folder->addChild($devnode);
	}
    }
}

# Subroutine to stop and restart the syncthing service
sub RestartSyncthing {
    # Stop the daemon
    system("systemctl --user stop syncthing.service");
    # Start the daemon
    system("systemctl --user start syncthing.service");
}

# Subroutine to write to config file
sub WriteConfig {
    my $doc = $_[0];
    open(my $fh, ">", $configfile) or die "ERROR: Could not open configuration file for writing";
    print $fh $doc->toString();
}

# Parse the XML
my $xmlparser = XML::LibXML->new();
my $confdoc = $xmlparser->parse_file($configfile);

# Handle command line interaction
# Get the action the user wants to take
my $action = $ARGV[0];
# Get the device id
my $id = $ARGV[1];
# switch on action
if($action =~ /list/){
    &PrintRegisteredDevices($confdoc);
} elsif ($action =~ /this/){
    &ThisDeviceID($confdoc);
} elsif ($action =~ /add/) {
    &AddDeviceID($id, $confdoc);
    &ShareFoldersToAll($confdoc);
    &WriteConfig($confdoc);
    &RestartSyncthing();
} elsif ($action =~ /remove/) {
    &RemDeviceID($id, $confdoc);
    &WriteConfig($confdoc);
    &RestartSyncthing();
} else {
    &PrintUsage();
}
