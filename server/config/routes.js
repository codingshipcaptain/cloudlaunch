const controller = require('./../controllers/controller');

module.exports = (app) => {
    app.get('/api/all', controller.index),
    app.get('/api/one/:id', controller.show),
    app.post('/api/new', controller.new),
    app.delete('/api/remove/:id', controller.destroy),
    app.put('/api/review/add/:id', controller.rcreate),
    app.put('/api/review/delete/:id', controller.rdestroy)
}
