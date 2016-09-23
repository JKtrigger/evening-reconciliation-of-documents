$( document ).ready(function() {
	
	$('#stext').keypress(function( event ) {
		if (event.keyCode == 13) {
			
		    $.ajax({
	            url: "./findMe",
			    type:'POST',
			    data: {'code': $('#stext').val()}, 
	            datatype:'html',
	            success: function(ans){
					console.log(ans)
				    res1 =''
					res2 =''
					res3 =''
					res4 =''
				    ans = ans.replace(/\s/g,'').split(';')
				    var i = 0;
				    for (i ;i < ans.length ; i++){
						if (ans[i].split(':')[0]=='scann'){
							if (ans[i].split(':')[1].length == 19){
								var a = ans[i].split(':')[1].replace(/\//g,'').slice(0,14)
								$('#'+a).remove()
								c = c.replace(a+',', "")
								c = c.replace(a, "")
							}
							if (ans[i].split(':')[1].length == 14){
							    $('#'+ans[i].split(':')[1]).remove()
							    c = c.replace(ans[i].split(':')[1], "")
							}
						}
						
						if (ans[i].split(':')[0]=='lenScann'){
							res1 = ans[i].split(':')[1]
						}
						if (ans[i].split(':')[0]=='lenNocann'){
							res2 = ans[i].split(':')[1]
						}
						if (ans[i].split(':')[0]=='lenUniqueScann'){
							res3 = ans[i].split(':')[1]
						}
						if (ans[i].split(':')[0]=='lenSUniqueNocann'){
							res4 = ans[i].split(':')[1]
						}
						if (res1 && res2 && res3 && res4){
							$('#cur').text(res1 +'/' +res2+'  '+res3+'/'+res4)
						}
						if (ans[i].split(':')[0]=='double'){
							$('#double').text($('#double').text() + ',' + ans[i].split(':')[1])
						}
						if (ans[i].split(':')[0]=='error'){
							$('#err').text($('#err').text() + ',' + ans[i].split(':')[1])
							
						}
				    }
				$('#stext').val('') ;
				
	           }
	        });    
		return false	
		}
		
	})
	$('#chechForm').submit( function(event) {return false});
	
	
	
});