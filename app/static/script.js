        function httpGet(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
            xmlHttp.send( null );
            return xmlHttp.responseText;
        }

        function clickedUpdate(e, a)
        {

                window.location.assign('/update/' + a);

        }

        function clickedDelete(e, a)
        {
            if(!confirm('Confirm delete?')) {
                e.preventDefault();
            }

            else{
                window.location.assign('/delete/' + a);
            }
        }

        // Based on https://www.mxcursos.com/blog/como-consultar-cep-utilizando-javascript/
        $(document).ready(function() {
                "use strict";

                const cep =  $("input[name = postalCode]");

           $("input[name = postalCode]").on('blur', function(e) {

                var validacep = /^[0-9]{8}$/;


                const value = cep.val().replace(/[^0-9]+/, '');

                if(validacep.test(cep.val())) {

                const url = 'https://cdn.apicep.com/file/apicep/'+ value.substring(0, 5) + '-' + value.substring(5, 8) + '.json';

                fetch(url)
                .then((response) => {
                  if (response.ok) {
                    return response.json();
                  }
                  throw new Error('Something went wrong');
                })
              .then( json => {


                  if( json.address ) {
                    $("input[name = street]").val(json.address);
                    $("input[name = city]").val(json.city);
                    $("input[name = state]").val(json.state);
                    $("input[name = country]").val('Brazil');
                  }


              })
              .catch((error) =>
              {

                    alert('Postal code not found, try again');
                    $("input[name = street]").val('');
                    $("input[name = city]").val('');
                    $("input[name = state]").val('');
                    $("input[name = country]").val('');
                    $("input[name = number]").val('');
                    $("input[name = postalCode]").val('');
              });



              }
              else
              {
                alert('Postal code must be XXXXXXXX')
                $("input[name = postalCode]").val('');
                $("input[name = street]").val('');
                $("input[name = city]").val('');
                $("input[name = state]").val('');
                $("input[name = country]").val('');
                $("input[name = number]").val('');
                $("input[name = postalCode]").val('');
              }

           });


        })