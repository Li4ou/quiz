let block;
let testet = [];


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// function f() {
//     block = document.getElementById('block');
//
//
// }


function nagrady() {
    let bloks_nagrady = document.getElementById('bloks_nagrady');
    if (bloks_nagrady.style.display === "none") {

        bloks_nagrady.style.display = 'block';

    } else {
        bloks_nagrady.style.display = 'none';

    }


}

function get_quiz_list() {
    testet = []
    // "Получение списка виктоин"
    $.ajax({
            url: 'api/quiz/?limit=10',
            merhod: 'get',
            dataType: 'json',
            success: function (data) {
                setTimeout(render_quiz_list, 500, data)
                get_nagrady()
                setTimeout(te, 500)


            }
        }
    )

}

function te() {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

}


function get_questions(next) {
    set_ansver()

    $.ajax({
            url: next,
            merhod: 'get',
            dataType: 'json',
            success: function (data) {
                let offset = data.offset + 1;
                let percent = offset * 100 / data.count;
                document.getElementById('block').innerHTML = '<div id="quiz" class="row"><div>\n' +
                    '    <div class="row">\n' +
                    '        <div class=" col text-start" style="margin-left: 0; margin-right: auto">\n' +
                    '            <h2 style="color: blue"><b>Вопрос</b>\n' +
                    '            </h2>\n' +
                    '        </div>\n' +
                    '        <div class="col text-end" style="color: blue">\n' +
                    '            <h2><b>' + offset + '/' + data.count + '</b></h2>\n' +
                    '        </div>\n' +
                    '\n' +
                    '        <div style="background-color: dimgrey;width: 100%;height: 10px; border-radius: 3px;padding: 0">\n' +
                    '            <div style="width:' + percent + '%; background-color: blue;height: 10px"></div>\n' +
                    '        </div>\n' +
                    '    </div>\n' +
                    '    <div>\n' +
                    `            <h1><b>${data.results[0].text} </b></h1>\n` +
                    '            <form id="answer" name="answer">\n' +
                    '\n' +
                    '                <div id="questions" class="btn-group-vertical w-100 gap-2" role="group">\n' +
                    '\n' +
                    '                </div>\n' +
                    '                <div class="mt-4" id="button">\n' +
                    '                </div>\n' +
                    '            </form>\n' +
                    '\n' +
                    '\n' +
                    '            </div>\n' +
                    '</div>\n'
                if (data.next != "'None'") {
                    $('#button').append('<input type="button" id="btn" class="btn btn-primary" onclick="get_questions(' + data.next + ')" value="Следующий вопрос">')

                } else {
                    $('#button').append(`<input type="button" id="btn" class="btn btn-primary" onclick="f1(${data.id})" value="Завершить виктарину">`)


                }
                data.results[0].answer.forEach(function (item) {
                    $('#questions').append('<input type="radio" class="btn-check" name="id" value="' + item.id + '" id="vbtn-radio-' + item.id + '"' +
                        'autocomplete="off"' +
                        'checked="">' +
                        '<label class="btn btn-outline-primary " for="vbtn-radio-' + item.id + '"' +
                        'style="vertical-align: inherit;"><b>' + item.text + '</b></label>')

                })


            }
        }
    )


}


function set_ansver() {
    answer_id = $("#answer").serialize().replace(/[^+\d]/g, '');
    if (answer_id != "") {
        testet.push(parseInt(answer_id))

    }


}


function f1(quiz_id) {
    set_ansver()
    data = {
        "quiz": quiz_id,
        "answer": testet,
    }
    $.ajax({
            url: 'api/result/',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(data),
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
                'Content-type': 'application/json',
            },
            success: function (data) {
                testet = []
                document.getElementById('block').innerHTML = `
                <div id="quiz" class="row"><div>
                    <div class="row">
                            <div class=" col text-start" style="margin-left: 0; margin-right: auto">
                                <h2 style="color: blue"><b>Результаты</b>
                                </h2>
                            </div>
                            <div class="col text-end" style="color: blue">
                                <h2><b>${data.correct}/${data.count}</b></h2>
                             </div>
                 
                            <div style="background-color: dimgrey;width: 100%;height: 10px; border-radius: 3px;padding: 0">
                                <div style="width:100 %; background-color: blue;height: 10px"></div>
                            </div>
                            <div>
                        </div>
                        <div class="row mt-4">
                        <div class="col"><img src="/static/image/robot.png" style="height: 300px"></div>
                        <div class="col"><div><h2><b>Ты  ответил на  ${data.correct} вопросов правильно  из  ${data.count} </b></h2></div>
                        <div id="dialog"></div>
                                         <div><button type="b   utton" class=" w-100 btn btn-primary" onclick="get_quiz_list()" >Вернуться на главную</button></div>
                        </div>
                        
                        </div>
                      
                  </div>                `


            },
            error: function (error) {
            }

        }
    )


}

// Вывод списка виктарин
function render_quiz_list(data) {
    document.getElementById('block').innerHTML = '<div id="quiz" class="row">' +
        '<div class="text-start" style="margin-left: 0; margin-right: auto">' +
        '<h2><b>Викторины</b></h2>'
    '</div>'

    '</div>'
    data.results.forEach(function (item) {
        let count = item.complexity;
        $('#quiz').append(`<div class="col" title=" Сложность:  ` + "&#9734;".repeat(count) + `"> <button type="button" class="btn btn-danger" onclick="get_questions( ${item.next})">${item.name}</button> </div>`)

    })
}


function get_nagrady() {

    $.ajax({
        url: 'api/nagrady/',
        type: 'GET',
        dataType: 'json',

        success: function (data) {
            document.getElementById('nagrady').innerHTML = "";
            data.results[0].achievements.forEach(function (item) {
                let count = item.lvl
                $('#nagrady').append(`<div class="col p-0"  data-bs-toggle="tooltip" data-bs-trigger="hover" title='<div class="pop">
       <h3 class="popover-title  ` + item.type + `"><b>` + item.title + `<b></b></b></h3>
       <div><b>Тип: <span class="` + item.type + `">` + item.type + `</span></b> </div>
       <div><b>Уровень:  ` + "\t&#9734;".repeat(count) + ` </b> </div>
       <div><b> Балы: ` + item.balls + `</b> </div>
       <div><b>Описание: ` + item.description + `</b> </div>
       </div>' data-bs-html="true"><img class="${item.type}" src="${item.image}" style="height: 120px"></div>`)

            })


        }

    })
}


