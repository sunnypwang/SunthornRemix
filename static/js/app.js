function predict(wak, method) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document
                .getElementById('prediction_wrapper')
                .classList.remove('loader')
            document.getElementById('prediction').innerHTML = this.responseText
            document.getElementById('predict_btn').classList.remove('disabled')
            console.log(document.getElementById('word').value)
        }
    }
    var isMobile = window.matchMedia('only screen and (max-width: 760px)')
        .matches

    url =
        'http://35.234.33.177:3000/predict?method=' +
        method +
        '&tok=' +
        document.getElementById('word').value +
        '&wak=' +
        wak +
        '&mobile=' +
        isMobile
    xhttp.open('GET', url, true)
    xhttp.send()
}

document.getElementById('predict_btn').addEventListener(
    'click',
    function() {
        document.getElementById('predict_btn').classList.add('disabled')
        document.getElementById('prediction').innerHTML = null
        document.getElementById('prediction_wrapper').classList.add('loader')

        wak = document.querySelector('input[name="wak"]:checked').value
        method = document.querySelector('input[name="method"]:checked').value
        predict(wak, method)
    },
    false
)
