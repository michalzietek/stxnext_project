$(() => {
  $(document).on('click', ".delete-player-btn", () => {
    player = $(this).data('id');
    if ($(this).attr('data-list-url')) {
      $('#modal-delete-player-warning-warning').data('list-url', $(this).attr('data-list-url'));
    }
    $('#modal-delete-player-warning').modal('show');
    $('#modal-delete-player-warning').find('button[id="delete-submit-btn"]').data('id', player);
  });
});

$('#modal-delete-player-warning').on('click', '#delete-submit-btn', () => {
  player = $(this).data('id');
  $.ajax({
    url: $(this).attr('data-url'),
    data: {
      'player': player
    },
    success: function() {
        location.reload();
    }
  });
});

$(function() {
    $(document).on('click', '.edit-player-btn', function() {
        player = $(this).data('id');
        console.log('jestem tutaj');
        $.ajax({
          url: $(this).attr('data-url'),
          type: 'GET',
          dataType: 'json',

          beforeSend: function() {
            $('#player-edit-modal').modal('show');
            $('#player-edit-modal').attr('data-id', player);
            console.log($(this).attr('data-url'));
          },
          success: function(data) {
            $('#player-edit-modal .modal-content').html(data.html_form);
          }
        });
    })
});

$(function () {
  $('#player-edit-modal').on('submit', '#ajax-player-edit-form', function() {
    var data = new FormData($('#ajax-player-edit-form')[0]);
    $.ajax({
        url: $(this).data('url'),
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,

        success: function(data) {
          if (data.form_is_valid) {
              $('#player-edit-modal').modal('hide');
              window.location.reload();
          }
        }
    });
    return false;
  });
});
