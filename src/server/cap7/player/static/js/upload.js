<script type="text/javascript">
  $(".upload").click(function(){

    $.ajax({
        type: post,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            alert('success');
        }
    });
    return false;
   });
</script>
