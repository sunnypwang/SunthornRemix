function predict(method, style, wak) {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document
                .getElementById('prediction_wrapper')
                .classList.remove('loader')
            var res = JSON.parse(this.responseText)
            console.log(res)
            if (res.status == 'ok') {
                document.getElementById('prediction').innerHTML = res.message
            } else if (res.status == 'error') {
                alert(res.message)
            }

            document.getElementById('predict_btn').classList.remove('disabled')
            console.log(document.getElementById('word').value)
        }
    }
    var isMobile = window.matchMedia('only screen and (max-width: 760px)')
        .matches

    url =
        'http://35.234.33.177:3000/predict?method=' +
        method +
        '&style=' +
        style +
        '&wak=' +
        wak +
        '&tok=' +
        document.getElementById('word').value +
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

        method = document.querySelector('input[name="method"]:checked').value
        style = document.querySelector('input[name="style"]:checked').value
        wak = document.querySelector('input[name="wak"]:checked').value

        predict(method, style, wak)
    },
    false
)
