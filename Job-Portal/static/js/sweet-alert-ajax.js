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
                $("#row_"+id).remove();
              } else if (route.includes('close')) {
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