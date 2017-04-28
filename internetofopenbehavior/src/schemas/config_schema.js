var SchemaObject = require('schema-object');

var Schedule = new SchemaObject({
	name: {
		type: String, 
		enum: ['pr', 'fr', 'ext', 'vr'],
		required: true
	},
	default: {
		type: Boolean,
		required: true
	},
	breakpoint: {
		type: Number,
		required: false
	},
	timeout: {
		type: Number,
		required: true
	},
	session_length: {
		type: Number,
		required: true
	},
	ratio: {
		type: Number,
		required: false
	}

}, {
	methods: {
		next_ratio: function() {
			var next_ratio = null;
			if(this.name == 'pr') {
				next_ratio = 5*(2.72**(this.breakpoint/5)-5);
			} else if(this.name == 'fr') {
				next_ratio = this.ratio;
			} else if(this.name == 'ext') {
				next_ratio = -1;
			} else if(this.name == 'vr') {
				next_ratio = this.ratio;
			}

			if(ratio == null) {
				console.err("There was an error calculating the next ratio for schedule: " + this.name);
			}

			return next_ratio;
		}
	}
});
