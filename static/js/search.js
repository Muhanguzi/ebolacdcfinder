$(document).ready(function(){ 


    var points = [];
    var map;
    var datax =[];
    var mypageIndex;
    var itemStart;
    var itemsEnd;
    var inforBoxContent = [];
    var lat;
    var lng;


     var icon_color = {
                                path: google.maps.SymbolPath.CIRCLE,
                                fillOpacity: 1.0,
                                fillColor: '#FF0000',
                                strokeOpacity: 1.0,
                                strokeColor: '#FFFFFF',
                                strokeWeight: 2.0, 
                                scale: 7
                            }
                   
     
     var styles =[
            {
                "featureType": "water",
                 "stylers": [
                 { "hue": "#003bff" }
                   ]
            },{
                "featureType": "road",
                 "stylers": [
                  { "visibility": "on" },
                { "saturation": -1 }
                    ]
            },{
                "featureType": "poi",
                "stylers": [
                { "visibility": "on" },
                { "saturation": 27 },
                { "hue": "#88ff00" }
                ]
            },{
                "featureType": "landscape",
                "stylers": [
                { "saturation": -3 }
                ]
            }
        ];
    var styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});
     
     var mapOptions2 = {
             
             zoom: 15,
             mapTypeControlOptions: {
             mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
             }
         
         }    

    function initiate_geolocation() {
            
         navigator.geolocation.getCurrentPosition(handle_geolocation_query);
    
    }
 
    function handle_geolocation_query(position){

            var distance;

            if (!$('input:radio[name=distance]:checked').val()){

                distance = 7;
        

            }else{

                distance = $('input:radio[name=distance]:checked').val();
            
     
            }

            $.ajax({
              type: "GET",
              url: "/search/",
              data: {lat:position.coords.latitude,lng:position.coords.longitude,dist:distance},
              dataType: "json",
              beforeSend: function() {
                    $('#map-major').empty();
                    $('#map-major').html("<img class='loader'src='/media/loading.gif' />");
                },
              success: function (data){

                     if(data.msg.length == 0){



                        $('#map-major').empty();
                        $('#map-major').append("<div id='biz_results_not_found'><h3>No results found matching your search area.</h3></div>");
                     
                           
                          
                     }else{


                         datax = data.msg;
                           
                            
                        $('#map-major').empty();
                        $('#map-major').append("<div id='biz_display_header'></div>");
                        $('#map-major').append("<div id='biz_display_wrapper'></div>");
                        $('#biz_display_wrapper').append("<div class='business_search_display'></div>");
                        $('#biz_display_wrapper').append("<div id='business_search_header'></div>");
                        $('#biz_display_wrapper').append("<div id='business_search_wrapper'><div class='col-sm-4' id='business_search_map'></div></div>");
                        $('#biz_display_wrapper').append("<div id='Pagination' class='pagination'></div>");
         
                         $("#Pagination").pagination(data.msg.length,{
                              items_per_page: 5, 
                              callback: pageselectCallback
                            });
  
                     }
                 }

               }); 
        
     
     }
    

    $('#search-nearest-care').click(function(){
      
        initiate_geolocation();



    });

     function bindInfoBox(marker,content) {
    
        var infobox = new InfoBox({
            content: content,
            disableAutoPan: false,
            maxWidth: 70,
            pixelOffset: new google.maps.Size(-22, -60),
            zIndex: null,
            boxStyle: {  
                width: "130px"   
            },
            closeBoxURL: ""
        });
        
      google.maps.event.addListener(marker, 'mouseover', function() {
        
            infobox.open(map, this);
        
      });
      google.maps.event.addListener(marker, 'mouseout', function() {
      
            infobox.close(map, this);
        
      });
      
     contentHover(marker,infobox);
        
     }

     function contentHover(marker,infobox){
    
        $('.business_summary').on( 'mouseover',  function() { 
            
            var y = parseInt(this.id);
         
                if( y === marker.get("id")){
                
                    infobox.open(map,marker);
                   
                    
                }
            
         } ).on('mouseout', function() {
      
                    infobox.close(map,marker);
        });
   
     }
     function addMarkers(startItem,endItem) {
    // when the map is initialized and the points have been initialized, add them to the map
        if ((map != null) && (points.length > 0)) {
            for (var i = startItem; i < endItem; i++) {
                    var marker = new google.maps.Marker({
                        map: map,
                        position: points[i],
                        icon: icon_color
                    });
                    marker.set("id", i);
                    bindInfoBox(marker,inforBoxContent[i]);
            }
        }
     }

     function pageselectCallback(page_index, jq){
                // Get number of elements per pagionation page from form
                
           var business_des_length = 100;
           var business_des;
           var truncated_description;
            
            mypageIndex = page_index+1;
            var items_per_page = 5;
            var startItem = page_index*items_per_page;
            var endItem= Math.min((page_index+1) * items_per_page, datax.length);
            var mypageIndexEnd = Math.ceil(datax.length/items_per_page);
            var newcontent = "<div>";
            itemsStart = startItem+1;
            itemsEnd = endItem;
            // Iterate through a selection of the content and build an HTML string
            for(var i=startItem;i<endItem;i++)
            {
            
              points.push(new google.maps.LatLng(datax[i].lat,datax[i].lng));
              newcontent += "<div class='business_summary' id='"+i+"'>";
              newcontent +=  "<div id='business_summary_detail'><a href='/d/"+datax[i].center_id+"' class='biz_summary_name'>"+datax[i].centerName+"</a></div><div>";
              newcontent +=  "<span>"+datax[i].roadAddress+"</span><br/>";
              newcontent +=  "<span class='country'>"+datax[i].country+" ,"+"</span><span class='country'>"+datax[i].city+" </span><br/>";
              newcontent +=  "<span class='glyphicon glyphicon-phone' id='search_tel'>"+datax[i].telephone+"</span><br/>"
              newcontent +=  "<span class='flag'><a href='/report/"+datax[i].center_id+"'>-Flag-</a></span>"
              newcontent +=  "</div></div></div>";

              inforBoxContent[i] = "<div class='infobox'><span class='infoboxContent'><a href='/d/"+datax[i].centerName+"'>"+datax[i].centerName+"</a></span><br/><span>"+datax[i].telephone+"</span></div>";  
                                
            }
            
            
            $('#Pagination').append("<label>Page "+mypageIndex+" of "+mypageIndexEnd+"</label>");
            $('#business_search_header').html("<label style='text-align:right;'>Showing "+itemsStart+" - "+itemsEnd+" of "+datax.length+"</label>");
            // Replace old content with new content
            
            $('.business_search_display').html(newcontent);
           
             map = new google.maps.Map(document.getElementById("business_search_map"), mapOptions2);
             map.mapTypes.set('map_style', styledMap);
             map.setMapTypeId('map_style');
             map.setCenter(points[0]);
             addMarkers(startItem,endItem);
             
             
            
            return false;
     }







});