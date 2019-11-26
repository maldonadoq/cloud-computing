/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */

const translate = require('@google-cloud/translate');

exports.translate = function(req, res){
    let language = req.body.language || 'es';
    translate.translate('Hello World', language,
        (err, translation) => {
            res.status(200).send(translation);
        });
}

// curl -H "Content-Type: application/json" -X POST -d '{"language":"es"}' https://us-central1-wide-graph-259823.cloudfunctions.net/function-translate