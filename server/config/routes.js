const controller = require('./../controllers/controller');

module.exports = (app) => {
    app.get('/api/all', controller.index),
    app.get('/api/one/:id', controller.show),
    app.post('/api/new', controller.new),
    app.put('/api/update/:id', controller.update),
    app.delete('/api/remove/:id', controller.destroy)
}
