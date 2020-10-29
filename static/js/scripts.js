$(document).ready(function(){
    var $group = $('.input-group');
    var $file = $group.find('input[type="file"]')
    var $fileDisplay = $group.find('[data-action="display"]');
    const sleep = milliseconds => {
            return new Promise(resolve => setTimeout(resolve, milliseconds));
        };
     $("#btnSubmit").click(function (event) {

                event.preventDefault();
                $("#btnSubmit").hide();
                $('#loading').show();
                var form = $('#fileUploadForm')[0];
                var data = new FormData(form);
                if($('#fileSelect').val().trim())
                {
                    $.ajax({
                    type: "POST",
                    enctype: 'multipart/form-data',
                    url: "/uploader",
                    data: data,
                    dataType:'json',
                    processData: false,
                    contentType: false,
                    cache: false,
                    timeout: 600000,
                    success: function (data) {

                        console.log("SUCCESS : ", data);
                        window.location.href = "/reconcile/"+data['filename'];

                    },
                    error: function (e) {

                        //$("#result").text(e.responseText);
                        console.log("ERROR : ", e);

                        //$("#btnSubmit").prop("disabled", false);

                    }
                });
                }
                else
                {
                    alert('Please Select A File!');
                    $("#btnSubmit").show();
                    $('#loading').hide();
                }

            });

    $("#fileUpload").click(function(){
        $('#Modal').modal('show');
        AjaxFileUpload();
    });
    var browseHandler = function(e) {
        //If you select file A and before submitting you edit file A and reselect it it will not get the latest version, that is why we  might need to reset.
        //resetHandler(e);
        $file.trigger('click');
        
      };
    $fileDisplay.on('click',  function(e) {
        if (event.which != 1) {
          return;
        }
        browseHandler();
      });
    $file.on('change', function(e) {
        var files = [];
        if (typeof e.currentTarget.files) {
          for(var i = 0; i < e.currentTarget.files.length; i++) {
            files.push(e.currentTarget.files[i].name.split('\\/').pop())
          }
        } else {
          files.push($(e.currentTarget).val().split('\\/').pop())
        }
        $fileDisplay.val(files.join('; ')) 
      });

});
