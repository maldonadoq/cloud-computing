import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

admin.initializeApp(functions.config().firebase);

/*
* Get Request
exports.hello = functions.https.onRequest((req, res) => {
    res.send('Hello World from Firebase');
});
*/


// Request Save item
exports.add = functions.https.onRequest((req, res) => {
    admin.firestore().collection('Items').add({
        text: req.query.text
    }).then(r => {
        res.send('Completed!\n');
    }).catch(e => {
        res.send('There was a error\n')
    })
});


exports.counter = functions.firestore.document('Items/{itemId}').onCreate((event) =>{
    const doc = admin.firestore().doc('Counter/Items');

    /*return new Promise((res, rej) => {
        doc.get().then((result) => {
            const info = { value: result.data().value + 1};

            doc.update(info).then(res).catch(rej)
        });
    });*/

    return doc.get().then((result) => {
        const info = {value: result.data()!.value + 1};
        return doc.update(info);
    });
})

// Url
// https://us-central1-functions-321be.cloudfunctions.net/add?text=Keyboard
