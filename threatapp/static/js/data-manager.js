function DataManager(api0,api1,api2) {

  //data fetched from the server; used for deep comparsion to determine notification for uppate 
  this.fetched_data = []
  //data that had been notified 
  this.current_data = []
  // data used for rendering in the table ui 
  this.displayed_data = []
  // the current  url for long polling 
  this.currentapi = api0
  // the restful url : 24 hours 
  this.api0 = api0  
  // the restful url : 7 days
  this.api1 = api1
  // the restful url : 4 weeks
  this.api2 = api2

  // below booleans for synchronization of long polling 

  this.firstTimeLoad = true
  this.ajaxing = false
  // for dropdown 
  this.select_reload = true

   /*  Main starter func*/ 
  this.start_service = function() {
    this.init_data()
      //retrieve and render table
      this.start_polling()
  }


  this.init_data = function() {
      this.currentapi = this.api0
      this.firstTimeLoad = true
      this.ajaxing = false
      this.select_reload = true
      
  }

    // Switch long polling url when users select dropdown
    this.choose_period = function(arg) {
      //pervent update inquiry dialog; will be reset in long polling process
      this.select_reload = true

      //switch long-polling url 
      if(arg == 0)
        this.currentapi = this.api0
      else if(arg == 1 ) 
        this.currentapi = this.api1
      else
        this.currentapi = this.api2
    }

    /**
    * Check data whether to be updated or not
    * Return ture, if equal;otherwise, return false
    */
    this.is_latest = function(cur_data, server_data) {
      //Performs a deep comparison between two values to determine if they are equivalent.
      //From https://lodash.com/docs/4.17.4#isEqual.
      return _.isEqual(cur_data, server_data)
    } 


    /* Render the popup when new changes detected in the  server*/
    this.render_popup = function(js_data) {
      if (confirm("Update detected changes?") == true) {
        this.confirm_popup(js_data)
      } else {
        this.dismiss_popup()
      }

    }

    /* Confirm popup to render data in the table */
    this.confirm_popup = function (js_data) {
      this.render_table_data(js_data)
    }

    /* dismiss popup */
    this.dismiss_popup = function() {
      return
    }


    /* Set up table structure by tabulator plugin;
    *  Handle sorting;
    *  Handle row color distribution 
    */
    this.setup_init_table = function() {

      // helper object for sorting rating level
      var level_sort_helper_dict = {"malicious": 5,"Malicious": 5,
      "high-risk": 4, "High-Risk": 4,
      "medium-risk": 3, "Medium-Risk":3,
      "low-risk": 2,"Low-Risk": 2,
      "clean": 1, "Clean": 1
    };

    $("#threat-table").tabulator({
      selectable:false,
      responsiveLayout : true, 
      height:"100%",// set height of table, this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
      layout:"fitColumns", //fit columns to width of table (optional)
      responsiveLayout:true,
      //start with rating sorted order
      initialSort:[
            {column:"rating", dir:"desc"}, //sort by rating 
      ],
      columns:[ //Define Table Columns
          {title:"File Name", field:"filename",align:"center"},
          {title:"Rating", field:"rating",align:"center", sorter:function(a, b){
            return level_sort_helper_dict[a]- level_sort_helper_dict[b] ;} },
            {title:"Action", field:"action", align:"center"},
            {title:"Submit-Type", field:"submit-type",align:"center"},
            {title:"Date", field:"date", sorter:"date",sorterParams:{format:"MMM DD, YYYY HH:mm:ss"}, align:"center"},
      ],

      // row color distribution
      rowFormatter:function(row){
        //row - row component

        var data = row.getData();
        switch(data.rating) {
          case "malicious":
          case "Malicious":
          row.getElement().css({"background-color":"Red"})
          break;
          case "high-risk":
          case "High-Risk":
          row.getElement().css({"background-color":"Orange"})
          break;
          case "medium-risk":
          case "Medium-Risk":
          row.getElement().css({"background-color":"LightSalmon"})
          break;
          case "low-risk":
          case "Low-Risk":
          row.getElement().css({"background-color":"LightGoldenRodYellow"})
          break;
          case "clean":
          case "Clean":
          row.getElement().css({"background-color":"LightCyan"})
          break;
          default:
          row.getElement().css({"background-color":"white"})
        }

      },
    });

  }


  /*render table data */
  this.render_table_data = function(js_data) {
      $("#threat-table").tabulator("clearData");
      //update displayed_data (model)
      that.displayed_data = JSON.parse(JSON.stringify(js_data))
      $("#threat-table").tabulator("setData", js_data);

      // in rating-level order
      $("#threat-table").tabulator("setSort", "rating", "desc");

      $(".tabulator-col-title").css("text-align","center")
      // //reset cell height
      // $(".tabulator-row").css("height","50px")
      // $(".tabulator-cell").css("height","50px")

      // // //center the text in table cells
      // $(".tabulator-cell").css("display","table-cell")
      // $(".tabulator-cell").css("vertical-align","middle")
      //$(".tabulator-tableHolder").css("background","white")

    }


  /* polling process */
  this.start_polling = function poll() {
      // capture scope; useful for calls from inner function
      that = this

      //poll periodically
      setInterval(function() {

        // if it is still polling, then quit the process
        if(that.ajaxing) {
          return
        }

        //set the process is in use 
        that.ajaxing = true 
        $.ajax({
          url : that.currentapi, //
          type : "GET", // http method

      //  // handle a successful response
          success : function(json) {
            //if new changes detected
            if(!that.is_latest(that.current_data,json)) {
              //update current data model cause users will get notified anyway
              that.current_data = JSON.parse(JSON.stringify(json))

              // first time set up
              if(that.firstTimeLoad) {
                that.firstTimeLoad = false
                that.setup_init_table()
                that.displayed_data = JSON.parse(JSON.stringify(json))
                that.render_table_data(json)
              }


              if(that.select_reload) {
                //if new  dropdown option is selected; no popup is required
                that.render_table_data(json) 
                that.select_reload = false         
              } else {
                that.render_popup(json)
              }
            }
          },

          //  // handle a non-successful response
          error : function(xhr,errmsg,err) {
            console.log("something went wrong.",err)
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          },
          // tear down when ajax is done
          complete: function() {
            that.ajaxing = false
          },
          timeout:2000

        });
        //period for long polling request
      },1000)


  }
}