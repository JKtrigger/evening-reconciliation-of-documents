$(document).ready(function(){

    $(".random > p").css({"visibility": "hidden","display":"None"})

   function getRandomArbitrary(min, max) {
       var num = Math.floor(Math.random() * (max - min)) + min;
       $(".random > p:nth-child("+num+")").css({"visibility": "visible","display":"block"});
   }
   getRandomArbitrary(1, 9)

     $("#keep_settings").click(function(){
     var names = $("td[data-name_category]");
     var for_json = [];
     for (var index = 0; index <names.length; index++){
        var cat_names = names[index].innerText
        var row = $("td[data-"+cat_names+"]").find("[checked]");
        var values=[]
        $.each(row, function(i,n) {values.push(n.value);});
        var obj = {"name":cat_names,"values":values}
        for_json.push(obj)
        console.log(obj)
     }
     var data = {"categories": JSON.stringify(for_json)};

        $.ajax({
            type: "POST",
            dataType: "html",
            data : data,
            url: "./colors_set",
            success: view_msg
        });

     });

    $("#create_new_category").click(function(){

    var elem = $("#keep_settings");
    enable_this(elem);
    var name_category = $("input[placeholder='common']").val().toUpperCase();
    var full_color_list = full_color_list_make();
    var values =  make_inputs_check_box(full_color_list,[]);
    var row = make_row(values,name_category);
    var parent = $('#groups_colors');
    patt =  /[A-Z]+/;
    if (patt.exec(name_category)==name_category){
    parent.append(row);
    }

    $("input[placeholder='common']").val("")
    });

    var colors_controller = $("[name = 'colors-controller']")
    colors_controller.find(".alert-info").remove();



    $.ajax({
        type: "GET",
        dataType: "json",
        url: "./static/color_loader/category.json",
        success: load_colors
    });

    $("#loads_categories").click(function(){
        $.ajax({
        type: "GET",
        dataType: "json",
        url: "./static/color_loader/category.json",
        success: loads_categories
        });

    })

    $('#color_add_button').click(function(){

         var msg = $('#msg').val().toUpperCase();
         $('#msg').val('');
         patt =  /[A-Z]+/
         var found_text = $('strong:contains("'+msg+'")');
         if (found_text.text()==msg){
            return
         }
         if (patt.exec(msg)==msg){
            add_alert(msg);}
         });

});
/*INIT COLORS PAGE*/

function load_colors(args){

    var colors = args.colors


    if (colors){
        for (color in colors){
        add_alert(colors[color])}
    }
}
function loads_categories(data){
    var categories = data.categories

    var full_color_list = full_color_list_make()

    if (categories){

        var parent = $('#groups_colors')
        parent.empty();

        for (category in categories){
            var name_category = categories[category].name
            var values = make_inputs_check_box(full_color_list,categories[category].values)
            var row = make_row(values,name_category)
            parent.append(row)
        }
    }
}

function add_alert(color){
            var child = `<div class="alert alert-info  alert-dismissable" style="width:90%;margin-bottom:0px;">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">
            &times;</a><strong>`+color+'</strong></div>'
            var colors_controller = $("[name = 'colors-controller']");
            $('#color_list_panel').after(child);
}

function setDifference(arg1, arg2){

  // arg2 - full list
  // arg1 - less list
  var set = new Set(arg1)
  var res = []

  for (var i = 0 ; i<arg2.length ; i++){
    if (set.has(arg2[i])){continue}
    else {
      res.push(arg2[i])
    }
  }
  return res
}

function make_inputs_check_box(full_list,checked_list){
    var sets = new Set(checked_list)
    var res = ''
    var disable = new Set()
    for (row in full_list){
    var custom = full_list[row]
    var checked = sets.has(custom)?"checked":""


    res += `
    <div class="checkbox">
        <label>
            <input type="checkbox" `+checked+` onclick=checked__(this) class=`+custom+"-COLOR"+` data-type="COLOR_CODE" value=`+custom+`>`+custom+`
            </input>
        </label>
    </div>
    `
    }
    $("input[data-type='COLOR_CODE']").unbind()
     $("input[data-type='COLOR_CODE']").change(function(){
        var elem = $("#keep_settings");
         enable_this(elem);
    });
    return res

}

function enable_this(element){
    $(element).prop( "disabled", false )
}
function make_row(values, name_category){
return `
            <tr data-row_categories=`+name_category+`>
            <td data-name_category>`+name_category+`</td>
            <td data-`+name_category+`>`+values+`</td>
            <td><button type="button" onclick="delete_row(this)" class="btn btn-default deleter">Удалить</button></td></tr>`

}function full_color_list_make(){
    var full_list = $('div.alert-info.alert > strong')
    var full_color_list = []
    for (i in full_list){
    if (full_list[i].innerText){full_color_list.push(full_list[i].innerText)}
    }
    return full_color_list
}
function delete_row(x){
   $(x).parent().parent().remove()
   enable_this($("#keep_settings"))
}
function keep_colors(){


    $.ajax({
        type: "POST",
        dataType: "html",
        data : {"colors": "".concat(full_color_list_make())},
        url: "./colors_set",
        success: view_msg
        });

}

function view_msg(arg){alert(arg)}

function checked__(elem){
    // Явно задаем статус
    elem.checked? $(elem).attr( "checked", true ): $(elem).attr( "checked", false );
}



