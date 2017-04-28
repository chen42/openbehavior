var SchemaObject = require('schema-object');

var Schedule = new SchemaObject({
	name: {
		type: String, 
		enum: ['pr', 'fr', 'ext', 'vr']
	},
	default: {
		type: Boolean
	}
});
