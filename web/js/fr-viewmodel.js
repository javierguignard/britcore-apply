var frlvm;

//Where is api?? Check this value
//const url = 'http://127.0.0.1:5000/';
const url = '';

ko.validation.rules['is_date'] = {
    validator: function (val) {
        var dt = moment(val, 'YYYY-MM-DD');
        console.log(dt);
        return dt.isValid();
    },
    message: 'The field is not a date (use format(\'YYYY-MM-DD\')'
};

ko.validation.rules['positive_field'] = {
    validator: function (val) {
        return !(isNaN(parseInt(val))) && parseInt(val) > 0;
    },
    message: 'The field needs a positive integer greater than 0'
};

ko.validation.registerExtenders();

ko.extenders.numeric = function(target, precision) {
    //create a writable computed observable to intercept writes to our observable
    var result = ko.pureComputed({
        read: target,  //always return the original observables value
        write: function(newValue) {
            var current = target(),
                roundingMultiplier = Math.pow(10, precision),
                newValueAsNum = isNaN(newValue) ? 0 : +newValue,
                valueToWrite = Math.round(newValueAsNum * roundingMultiplier) / roundingMultiplier;

            //only write if it changed
            if (valueToWrite !== current) {
                target(valueToWrite);
            } else {
                //if the rounded value is the same, but a different value was written, force a notification for the current field
                if (newValue !== current) {
                    target.notifySubscribers(valueToWrite);
                }
            }
        }
    }).extend({ notify: 'always' });

    //initialize with current value to make sure it is rounded appropriately
    result(target());

    //return the new computed observable
    return result;
};

ko.bindingHandlers.datePicker = {
    /*
    THIS FUNCTION CREATE A BINGING FOR DATEPICKER
     */
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var unwrap = ko.utils.unwrapObservable;
        var dataSource = valueAccessor();
        var binding = allBindingsAccessor();
        var options = {
            keyboardNavigation: true,
            todayHighlight: true,
            autoclose: true,
            startDate: '-1s',
            format: 'yyyy-mm-dd'
        };
        if (binding.datePickerOptions) {
            options = $.extend(options, binding.datePickerOptions);
        }
        $(element).datepicker(options);
        $(element).datepicker('update', dataSource());
        $(element).on("changeDate", function (ev) {
            var observable = valueAccessor();
            if ($(element).is(':focus')) {
                // Don't update while the user is in the field...
                // Instead, handle focus loss
                $(element).one('blur', function (ev) {
                    var dateVal = $(element).datepicker("getDate");
                    observable(dateVal);
                });
            }
            else {
                observable(ev.date);
            }
        });
        //handle removing an element from the dom
        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            $(element).datepicker('remove');
        });
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        $(element).datepicker('update', value);
    }
};

function frViewModel() {
    var self = this;

    //WORK WITH ARRAYS
    self.frList = ko.observableArray();
    self.list_of_clients = ko.observableArray();
    self.list_of_areas = ko.observableArray();

    //WORK WITH MODEL
    self.id = ko.observable(false);
    self.title = ko.observable().extend({ required: true });
    self.description = ko.observable();
    self.client_id = ko.observable().extend({ required: true });
    self.client_priority = ko.observable().extend({ numeric: 1,positive_field:true, required: true });
    self.product_area = ko.observable().extend({ required: true });
    self.date_target = ko.observable().extend({ is_date: true,required: true });

    self.clear_model = function () {
        /*
        CLEAR MODEL DATA
         */
        self.id(false);
        self.title('');
        self.description('');
        self.client_id('');
        self.client_priority(1);
        self.product_area('');
        self.date_target(new Date())
    };

    self.load_model = function (id) {
        /*
        LOAD MODEL DATA
         */
        var model = self.getFrById(parseInt(id));
        if (model == '') {
            self.clear_model();
            return false;
        }

        self.id(model.id());
        self.title(model.title());
        self.description(model.description());
        self.client_id(model.client_id());
        self.client_priority(model.client_priority());
        self.product_area(model.product_area());
        self.date_target(model.date_target())
    };
    self.getFrById = function (id) {
        /*
        GET MODEL FROM LIST
         */
        return ko.utils.arrayFirst(self.frList(), function (fr) {
            return fr.id() === id;
        }) || '';
    };

    self.delete = function(){
        /*

         */
        $.ajax({
                url: url + '/api/feature_requests/' + self.id()+'/',
                type: 'DELETE',
                success: function (result) {
                    create_message('Delete complete');
                    self.clear_model();
                    self.getFrs();
                    self.goToList();
                }
            });
    };

    self.save = function () {
        var dt = moment(self.date_target()).format('YYYY-MM-DD');
        data = {
            title: self.title(),
            description: self.description(),
            client_id: self.client_id(),
            client_priority: self.client_priority(),
            product_area: self.product_area(),
            date_target: dt,
        };
        if (self.id() > 0) {
            //Update item
            $.ajax({
                url: url + '/api/feature_requests/' + self.id() + '/',
                type: 'PUT',
                data:JSON.stringify(data),
                contentType: 'application/json',
                success: function (result) {
                    create_message('Update complete');
                    self.id(result.id);
                    self.getFrs();
                }
            });

        } else {
            //Add new fr
            $.post(url + "/api/features_requests/",
                data).success(function (data) {
                    create_message('Create complete');
                    self.id(data.id);
                    self.getFrs();
                }
            ).error(function(a,b,c){
                if (a.status==402){
                    create_error('Alredy exists the priotiry for this client');
                }else {
                    if (a.status==401) {
                        create_error('Please, check params');
                    }
                    else {
                        create_error('Error, please contact administrator');
                    }
                }



            });


        }

    };


    //CONSUME REST API

    self.clients_to_map = function () {
        var lst = [];

        for (i in self.list_of_clients()) {
            if (i.startsWith('__')) {
                continue
            }
            var map = {};
            map.idx = i;
            map.client = self.list_of_clients()[i];
            lst.push(map)

        }
        return lst;

    };
    self.getClientById = function (id) {
        var client = 'not found';
        for (i in self.list_of_clients()) {
            if (i == id) {
                client = self.list_of_clients()[i]();

            }

        }
        return client;
    };
    self.areas_to_map = function () {
        var lst = [];

        for (i in self.list_of_areas()) {

            if (i.startsWith('__')) {
                continue
            }
            var map = {};
            map.idx = i;
            map.area = self.list_of_areas()[i];
            lst.push(map)

        }
        return lst;

    };
    self.getAreaById = function (id) {
        var client = 'not found';
        for (i in self.list_of_areas()) {
            if (i == id) {
                client = self.list_of_areas()[i]();

            }

        }
        return client;
    };
    self.getFrs = function () {
        /*
        CALL TO APIS
         */
        $.getJSON(url + '/api/areas/').then(function (data) {
            self.list_of_areas(ko.mapping.fromJS(data));
        });

        $.getJSON(url + '/api/clients/').then(function (data) {
            self.list_of_clients(ko.mapping.fromJS(data));
        });

        $.getJSON(url + '/api/features_requests/').then(function (data) {
            var observableData = ko.mapping.fromJS(data);
            var array = observableData();
            self.frList(array);
        });


    };

    //FUNCTIONS
    self.get_from_list = function (id) {
        for (i in self.frList) {
            if (self.frList[i].id == id) {
                return self.frList[i]
            }
        }
        return null;
    };


    //MAKE AS ONE PAGE
    self.view_list = ko.observable(true);
    self.view_one = ko.observable(false);
    self.goToNewEdit = function (id) {
        location.hash = '/crud/' + id
    };
    self.goToList = function () {
        location.hash = '/list'
    };


    Sammy(function () {
        this.get('/list', function () {
            self.getFrs();
            self.view_list(true);
            self.view_one(false);
        });

        this.get('/crud/:id', function () {
            self.getFrs();
            self.load_model(this.params.id);
            self.view_list(false);
            self.view_one(true);
        });

        this.get('', function () {
            this.app.runRoute('get', '/')
        });
    }).run();
}

function create_message(message){
    /*
    CREATE AN INFO MESSAGE
     */
    create_message_type(message,'info');
}

function create_error(message){
    /*
    CREATE AN ERROR MESSAGE
     */
    create_message_type(message,'warning');
}

function create_message_type(message, type){
    /*
    CREATE AND SHOW MESSAGE
     */
    $('#message').html(message);
    $('.alert').removeClass('alert-info');
    $('.alert').removeClass('alert-waning');
    $('.alert').addClass('alert-'+ type);
    $('.alert').show();
    setTimeout(function(){$('.alert').hide()}, 2000);

}


$(document).ready(function () {
    /*
    INITIALIZE JAVASCRIPT
     */
    frlvm = new frViewModel();
    ko.applyBindings(frlvm);
    frlvm.getFrs();
    $('.alert').hide()
});