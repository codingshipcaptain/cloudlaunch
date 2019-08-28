const mongoose = require('mongoose');

const OneSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, "Name Required"],
        minlength: [3, "Name must be 3 characters or longer"]
    },
    type: {
        type: String,
        required: [true, "Type Required"],
        minlength: [3, "Type must be 3 characters or longer"]
    },
    description: {
        type: String,
        required: [true, "Description Required"],
        minlength: [3, "Description must be 3 characters or longer"]
    },
    likes: {type: Number, default: 0},
    skills: {
        type: [String],
        maxlength: [3, "Max of three skills allowed."]
    },
}, {timestamps: true});

mongoose.model('One', OneSchema);
module.export = OneSchema;
