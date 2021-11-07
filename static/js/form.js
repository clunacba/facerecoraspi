$(document).ready(function() {
	$('#iss').hide();
	var slider = document.getElementById("resolucionRange");
	var output = document.getElementById("showResolucion");
	output.innerHTML = slider.value;

	slider.oninput = function() {
	  output.innerHTML = this.value;
	}
	var slider2 = document.getElementById("distanciamientoRange");
	var output2 = document.getElementById("showDistanciamiento");
	output2.innerHTML = slider2.value;

	slider2.oninput = function() {
	  output2.innerHTML = this.value;
	}
	$('input[id*=\"inlineRadio\"]').change(function(){
		var valor = $(this).val();
		$('#'+valor).show();
	});
	$('#resolucionRange').change(function(){
  		$('#distanciamientoRange').attr("max",$('#resolucionRange').val());
	});
	$('input[name="ISSip"]').on('change',function(){
		$('input[name="ISSpuerto"]').prop("disabled", true);
		if ($(this).val()) { 
			$('input[name="ISSpuerto"]').prop("disabled", false);
		}
	});
	$('input[name="ISSpuerto"]').on('change',function(){
		$('select[name="ISSevento"]').prop("disabled", true);
		if ($(this).val()) { 
			$('select[name="ISSevento"]').prop("disabled", false);
		}
	});
	$('form').on('submit', function(event) {
		var camera = 0;
		var iss = false;
		if($('#webcamInput').val()) {
			camera = $('#webcamInput').val();
		} else if($('#rtspInput').val()) {
			camera = $('#rtspInput').val();
		} else if ($('#videoFile').val()) {
			camera = $('#videoFile').val();
		}
		if($('input[name="ISSip"]').val() && $('input[name="ISSpuerto"]').val() && $('select[name="ISSevento"]').val()) {
			iss = $('input[name="ISSip"]').val()+':'+$('input[name="ISSpuerto"]').val()+'/'+$('select[name="ISSevento"]').val()+'?';
		}
		$.ajax({
			data : {
				webcam : camera,
				resolucion : $('#resolucionRange').val(),
				distanciamiento : $('#distanciamientoRange').val(),
				cliente : iss
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			} else {
				console.log("Cambios 3");
				d = new Date();
				$('#video_validado').find('img').attr("src", "/video_feed?"+d.getTime());
				/**$('#successAlert').text(data.name).show();**/
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});
});