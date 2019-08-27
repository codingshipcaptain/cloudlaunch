const mongoose = require('mongoose');

const OneSchema = new mongoose.Schema({
    title: {type: String, required: true, minlength: 3},
    rating: {type: Number},
    reviews: [{name: String, rating: Number, ureview: String}]
}, {timestamps: true});

mongoose.model('One', OneSchema);
module.export = OneSchema;
