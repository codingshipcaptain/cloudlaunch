const mongoose = require('mongoose');
const One = mongoose.model('One');
const Review = mongoose.model('Review');


module.exports = {
    index: (req, res) => {
        One.find()
        .then(thing => res.status(200).json(thing))
        .catch(err => res.status(500).json(err))
    },
    new: (req, res) => {
        console.log("At controller: ", req.body);
        Review.create(req.body.review)
        .then(thing => {
            res.json({good: true, tobj: thing});
            One.create(req.body.one)
            .then(thing => res.json({good: true, tobj: thing}))
            .catch(err => res.json({good: false, tobj: err}))
        })
        .catch(err => res.json({good: false, tobj: err}))

    },
    show: (req, res) => {
        const { id } = req.params;
        One.findOne({_id: id})
        .then(thing => res.status(200).json(thing))
        .catch(err => res.status(500).json(err))
    },
    destroy: (req, res) => {
        const { id } = req.params;
        console.log(id);
        One.deleteOne({_id: id})
        .then(thing => res.status(200).json(thing))
        .catch(err => res.status(500).json(err))
    },
    rcreate: (req, res) => {
        console.log("Total Data package: ", req.body);
        Review.create(req.body.treview)
        .then(nada => {
            const { id } = req.params;
            let count = req.body.tmovie.reviews.length;
            let sum = 0;
            for(var i = 0; i < count; i++){
                sum += parseInt(req.body.tmovie.reviews[i].rating);
            }
            console.log("Count: ", count);
            console.log("SUM: ", sum);
            sum += parseInt(req.body.treview.rating);
            console.log("SUM: ", sum);
            count++;
            console.log("Count: ", count);
            let nrating = sum/count;
            console.log("NRATING: ", nrating);
            console.log("this review: ", req.body.treview);
            One.updateOne({_id: id}, {$push: {reviews: req.body.treview}, $set: {rating: nrating} } )
            .then(thing => res.json({good: true, tobj: thing}))
            .catch(err => res.json({good: false, tobj: err}))
        })
        .catch(err => res.json({good: false, tobj: err}))

    },
    rdestroy: (req, res) => {
        console.log("**********");
        const { id } = req.params;
        console.log(id);
        Review.deleteOne(req.body)
        .then(thing => {
            console.log(req.body.name);
            One.updateOne({_id: id}, {$pull: {reviews: {name: req.body.name}}})
            .then(thing => res.status(200).json(thing))
            .catch(err => res.status(500).json(err))
        })
        .catch(err => res.json({good: false, tobj: err}))
    }
}
