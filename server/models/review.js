const mongoose = require('mongoose');

const ReviewSchema = new mongoose.Schema({
    name: {type: String, required: true, minlength: 3},
    ureview: {type: String, required: true, minlength: 3},
    rating: {type: Number, required: true},
}, {timestamps: false});

mongoose.model('Review', ReviewSchema);
module.export = ReviewSchema;
