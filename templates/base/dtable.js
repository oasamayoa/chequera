<script>
$(function() {

  $("#f1, #f2").datetimepicker({
    format: 'Y-m-d',
    timepicker:false

  });


    $('.table').DataTable({
      "scrollX": true,
      "scrollY": 400,
      "ordering": false,
      "responsive": true,

      "language": {
        "sProcessing": "Procesando...",
        "sLengthMenu": "Mostrar _MENU_ registros",
        "sZeroRecords": "No se encontraron resultados",
        "sEmptyTable": "Ningún dato disponible en esta tabla",
        "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
        "sInfoPostFix": "",
        "sSearch": "Buscar:",
        "sUrl": "",
        "sInfoThousands": ",",
        "sLoadingRecords": "Cargando...",
        "oPaginate": {
            "sFirst": "<span class='fa fa-angle-double-left'></span>",
            "sLast": "<span class='fa fa-angle-double-right'></span>",
            "sNext": "<span class='fa fa-angle-right'></span>",
            "sPrevious": "<span class='fa fa-angle-left'></span>"
        },
        "oAria": {
            "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
        }
      }
    });
  });

  </script>
