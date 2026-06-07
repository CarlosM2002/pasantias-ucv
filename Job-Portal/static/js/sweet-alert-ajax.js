function call_sw_alert_func(route, id, message){
    // var CSRF_TOKEN = $('meta[name="csrf-token"]').attr('content');
    
    swal({
      title: "¿Estás seguro?",
      text: message,
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then((willDelete) => {
      if (willDelete) {
        // var CSRF_TOKEN = `{{ csrf_token() }}`;
        // console.log(CSRF_TOKEN);
        $.ajax({
            type: 'GET',
            url: route,
            // data : {'_method' : 'DELETE', '_token' : CSRF_TOKEN },
            success : function(data) {
              if (route.includes('delete')) { 
                swal({
                  title: "¡Borrado!",
                  text: "Tu oferta ha sido eliminada!",
                  icon: "success",
                  button: "Done",
                });
                // Try removing by specific prefixes to avoid id collisions between models
                var removed = false;
                if (route.includes('delete-bookmark')) {
                  var $b = $("#bookmark_row_"+id);
                  if ($b.length) { $b.remove(); removed = true; }
                }  else if  (route.includes('delete-application')) {
                  var $a = $("#application_row_"+id);
                  if ($a.length) { $a.remove(); removed = true; }
                }
                // Fallback: try removing generic row or both prefixes
                if (!removed) {
                  var $row = $("#bookmark_row_"+id);
                  if ($row.length) { $row.remove(); removed = true; }
                  var $row2 = $("#application_row_"+id);
                  if ($row2.length) { $row2.remove(); removed = true; }
                }
                if (!removed) {
                  // If there's no table row (e.g. we're on the job detail page), reload to update buttons
                  location.reload();
                }
              } else if(route.includes('close')) {
                swal({
                  title: "¡Hecho!",
                  text: "Tu oferta ha sido marcada como cerrada!",
                  icon: "success",
                  button: "Done",
                });
                $("#change_job_status_"+id).html('<a class="text-white btn btn-success btn-sm" role="button">Closed</a>')
              } else if (route.includes('privileges')) {
                swal({
                  title: "¡Hecho!",
                  text: "Los privilegios se han actualizado.",
                  icon: "success",
                  button: "Done",
                }).then(function() {
                  location.reload();
                });
              }
            },

            error : function () {
                swal({
                    title: '¡Ocurrió un error inesperado!',
                    // text: data.message,
                    timer: '1500'
                })
            }
        });
      } else {
        swal("No se borró tu oferta!");
      }
    });
  }