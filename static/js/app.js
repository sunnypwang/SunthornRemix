function predict(method, style, temp, wak) {
    var xhttp = new XMLHttpRequest()

    var isMobile = window.matchMedia('only screen and (max-width: 760px)')
        .matches

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document
                .getElementById('prediction_wrapper')
                .classList.remove('loader')
            var res = JSON.parse(this.responseText)
            console.log(res)
            if (res.status == 'ok') {
                if (isMobile) {
                    document.getElementById(
                        'prediction'
                    ).innerHTML = res.message.replace(/ /g, '<br>')
                } else {
                    document.getElementById('prediction').innerHTML =
                        res.message
                }
            } else if (res.status == 'error') {
                alert(res.message)
            }

            document.getElementById('predict_btn').classList.remove('disabled')
            console.log(document.getElementById('word').value)
        }
    }

    url =
        'http://localhost:3000/predict?method=' +
        method +
        '&style=' +
        style +
        '&temp=' +
        temp +
        '&wak=' +
        wak +
        '&tok=' +
        document.getElementById('word').value
    xhttp.open('GET', url, true)
    xhttp.send()
}

function hideTemp() {
    document.getElementById('tempRange').classList.add('hide')
}

function showTemp() {
    document.getElementById('tempRange').classList.remove('hide')
}

document.getElementById('predict_btn').addEventListener(
    'click',
    function() {
        document.getElementById('predict_btn').classList.add('disabled')
        document.getElementById('prediction').innerHTML = null
        document.getElementById('prediction_wrapper').classList.add('loader')

        method = document.querySelector('input[name="method"]:checked').value
        style = document.querySelector('input[name="style"]:checked').value
        temp = document.getElementById('tempRange').value
        wak = document.querySelector('input[name="wak"]:checked').value

        predict(method, style, temp, wak)
    },
    false
)
