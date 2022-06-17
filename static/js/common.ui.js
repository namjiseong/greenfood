//퍼센트 비율 갱신 함수
function tag (end, tag) {
			

    let progress = document.getElementById(tag)
    let interval = 1
    let updatesPerSecond = 2000 / 180
    
    
    function animator () {
        if(end > 100){
            end = 100
        }
        progress.style.width = (parseInt(progress.style.width.substring(0,2)) + interval) + '%';

        if ( (parseInt(progress.style.width.substring(0,2)) + interval) < end){
            setTimeout(animator, updatesPerSecond);
        } else { 
            progress.style.width = end + '%'
        }
    }
  
    setTimeout(() => {
      animator()
    }, updatesPerSecond)
}
function tag_de (end, tag) {
			

    let progress = document.getElementById(tag)
    let interval = 1
    let updatesPerSecond = 2000 / 180
    
    
    function animator () {
        if(end < 0){
            end = 0
        }
        progress.style.width = (parseInt(progress.style.width.substring(0,2)) - interval) + '%';

        if ( (parseInt(progress.style.width.substring(0,2)) + interval) > end){
            setTimeout(animator, updatesPerSecond);
        } else { 
            progress.style.width = end + '%'
        }
    }
  
    setTimeout(() => {
      animator()
    }, updatesPerSecond)
}




function view_p(){
    
    var kal = 0;
    for (let i = 0; i < kal_list.length; i++) {
        kal += kal_list[i];
    }
    kal = Math.round(kal/2300 * 100) ;
    document.getElementById( 'kal' ).style.width = 0+'%';
    tag(kal, 'kal');
    var tan = 0;
    for (let i = 0; i < tan_list.length; i++) {
        tan += tan_list[i];
    }
    tan = Math.round(tan/324 *100);
    document.getElementById( 'tan' ).style.width = 0 +'%';
    tag(tan, 'tan');
    var dan = 0;
    for (let i = 0; i < dan_list.length; i++) {
        dan += dan_list[i];
    }
    dan = Math.round(dan/55 * 100);
    document.getElementById( 'dan' ).style.width = 0 +'%';
    tag(dan, 'dan');
    var ji = 0;
    for (let i = 0; i < ji_list.length; i++) {
        ji += ji_list[i];
    }
    ji = Math.round(ji/54 * 100);
    document.getElementById( 'ji' ).style.width = 0 +'%';
    tag(ji, 'ji');

    

    document.getElementById('kal_p').innerHTML=kal + '%';
    document.getElementById('tan_p').innerHTML=tan+'%';
    document.getElementById('dan_p').innerHTML=dan+'%';
    document.getElementById('ji_p').innerHTML=ji+'%';
}

//음식리스트 전송함수
function totext(){
    var inputt = document.getElementById('f_list');
    var f_list = "";
    for (let i = 0; i < list_f.length; i++) {
        f_list = f_list +" "+ list_f[i]
    }
    inputt.setAttribute('value', f_list);
    
}

//음식목록 추가 함수
function ad_food(food_name){
    var li = document.createElement("li");
    li.setAttribute('id', food_name);

    var span = document.createElement('span');
    span.setAttribute('class', 'name_food');
    span.innerHTML= food_name;
    var span2 = document.createElement('span');
    var span3 = document.createElement('span');
    span3.innerHTML= "  ";
    span.appendChild(span3);
    span2.setAttribute('id', food_name +'count');
    span2.innerHTML= 1;
    span.appendChild(span2);
    
    var bu1 = document.createElement('button');
    bu1.setAttribute('class', "btn_add");
    bu1.innerHTML='&#43;';
    bu1.setAttribute('onclick', 'another_add_food("'+food_name+'")');
    
    span_mini = document.createElement('span');
    span_mini.setAttribute('class', 'blind');
    span_mini.innerHTML = "추가";

    var bu2 = document.createElement('button');
    bu2.setAttribute('class', "btn_remove");
    bu2.innerHTML ='&#215;';
    bu2.setAttribute('onclick', 'de_food("'+food_name+'")');

    span_mini2 = document.createElement('span');
    span_mini2.setAttribute('class', "blind");
    span_mini2.innerHTML = "삭제";
    bu2.appendChild(span_mini2);
    span.appendChild(bu2);


    bu1.appendChild(span_mini);
    span.appendChild(bu1);
    li.appendChild(span);
    document.getElementById("abc").appendChild(li);
    totext()
}

//제거함수
function de_food(food_name){
    //제거
    var target = document.getElementById(food_name);
    var parent = target.parentElement; 
    parent.removeChild(target);
    // 타겟 인덱스 반환
    var index = list_f.indexOf(food_name);
    // 타겟 제외한 리스트 반환
    list_f = list_f.filter((element) => element !== food_name);
    //리스트에서 제거
    kal_list.splice(index, 1);
    dan_list.splice(index, 1);
    tan_list.splice(index, 1);
    ji_list.splice(index, 1);
    //제거된 리스트 기반으로 퍼센트 표시
    var kal = 0;
    for (let i = 0; i < kal_list.length; i++) {
        kal += kal_list[i];
    }
    kal = Math.round(kal/2300 * 100) ;
    //document.getElementById( 'kal' ).style.width = kal+'%';
    tag_de(kal, 'kal')
    var tan = 0;
    for (let i = 0; i < tan_list.length; i++) {
        tan += tan_list[i];
    }
    tan = Math.round(tan/324 *100);
    //document.getElementById( 'tan' ).style.width = tan +'%';
    tag_de(tan, 'tan')
    var dan = 0;
    for (let i = 0; i < dan_list.length; i++) {
        dan += dan_list[i];
    }
    dan = Math.round(dan/55 * 100);
    //document.getElementById( 'dan' ).style.width = dan +'%';
    tag_de(dan, 'dan')
    var ji = 0;
    for (let i = 0; i < ji_list.length; i++) {
        ji += ji_list[i];
    }
    ji = Math.round(ji/54 * 100);
    //document.getElementById( 'ji' ).style.width = ji +'%';
    tag_de(ji, 'ji')

    

    document.getElementById('kal_p').innerHTML=kal + '%';
    document.getElementById('tan_p').innerHTML=tan+'%';
    document.getElementById('dan_p').innerHTML=dan+'%';
    document.getElementById('ji_p').innerHTML=ji+'%';

    totext()
}

// 추가 함수
function another_add_food(food_name){
    // 타겟 인덱스 반환
    var index = list_f.indexOf(food_name);
    //2배로 증가
    kal_list[index] = kal_list[index] * 2;
    dan_list[index] = dan_list[index] * 2;
    tan_list[index] = tan_list[index] * 2;
    ji_list[index] = ji_list[index] * 2;
    //수정된 리스트 기반으로 퍼센트 표시
    var kal = 0;
    for (let i = 0; i < kal_list.length; i++) {
        kal += kal_list[i];
    }
    kal = Math.round(kal/2300 * 100) ;
    //document.getElementById( 'kal' ).style.width = kal+'%';
    tag(kal, 'kal')
    var tan = 0;
    for (let i = 0; i < tan_list.length; i++) {
        tan += tan_list[i];
    }
    tan = Math.round(tan/324 *100);
    //document.getElementById( 'tan' ).style.width = tan +'%';
    tag(tan, 'tan')
    var dan = 0;
    for (let i = 0; i < dan_list.length; i++) {
        dan += dan_list[i];
    }
    dan = Math.round(dan/55 * 100);
    //document.getElementById( 'dan' ).style.width = dan +'%';
    tag(dan, 'dan')
    var ji = 0;
    for (let i = 0; i < ji_list.length; i++) {
        ji += ji_list[i];
    }
    ji = Math.round(ji/54 * 100);
    //document.getElementById( 'ji' ).style.width = ji +'%';
    tag(ji, 'ji')

    

    document.getElementById('kal_p').innerHTML=kal + '%';
    document.getElementById('tan_p').innerHTML=tan+'%';
    document.getElementById('dan_p').innerHTML=dan+'%';
    document.getElementById('ji_p').innerHTML=ji+'%';

    var count = document.getElementById(food_name + 'count');
    count.innerHTML = (parseInt(count.innerHTML) + 1);
    
    totext()
}

function new_food(food_name){
    var parent = window.parent.document;
    parent.getElementsByClassName('inp_search')[0].value = food_name;
    console.log(parent.getElementsByClassName('inp_search')[0].value);
    parent.getElementById('검색').submit();
}