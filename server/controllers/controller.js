const mongoose = require('mongoose');
const One = mongoose.model('One')


module.exports = {
    index: (req, res) => {
        One.find().sort({type: 1})
        .then(thing => res.status(200).json(thing))
        .catch(err => res.status(500).json(err))
    },
    new: (req, res) => {
        var find;
        One.findOne({name: req.body.name})
        .then(data => {
            if(data == null){
                console.log("At controller: ", req.body);
                One.create(req.body)
                .then(thing => res.json({good: true, tobj: thing}))
                .catch(err => {
                    let errors = [];
                    for(let i in err.errors) {
                      console.log(i);
                      console.log('*'.repeat(50));

                      console.log(err.errors[i]);
                      errors.push({[i]: err.errors[i].message})
                    }
                    res.json({good: false, tobj: errors})
                })
            }
            else {
                console.log(data);
                res.json({good: false, tobj: [{name:"Name in use"}]})
            }
        })
        .catch(err =>res.json({good: false, tobj: errors}))
    },
    show: (req, res) => {
        const { id } = req.params;
        One.findOne({_id: id})
        .then(thing => res.status(200).json(thing))
        .catch(err => res.status(500).json(err))
    },
    update: (req, res) => {
        const { id } = req.params;
        var find;
        One.findOne({name: req.body.name})
        .then(data => {
            if(data == null || data._id == id){
                console.log("At controller: ", req.body);
                One.updateOne({_id: id}, req.body, {runValidators: true})
                .then(thing => res.json({good: true, tobj: thing}))
                .catch(err => {
                    let errors = [];
                    for(let i in err.errors) {
                      console.log(i);
                      console.log('*'.repeat(50));

                      console.log(err.errors[i]);
                      errors.push({[i]: err.errors[i].message})
                    }
                    res.json({good: false, tobj: errors})
                })
            }
            else {
                console.log(data);
                res.json({good: false, tobj: [{name:"Name in use"}]})
            }
        })
        .catch(err =>res.json({good: false, tobj: errors}))
    },
    destroy: (req, res) => {
        const { id } = req.params;
        console.log(id);
        One.deleteOne({_id: id})
        .then(thing => res.status(200).json(thing))
        .catch(err => res.status(500).json(err))
    }
}
