(function(_){
	 angular.module('cooperativa.contabilidad',['ngAnimate'])

        .factory('ContabiliadService',['$http','$q','$filter', function ($http, $q, $filter) {
        	 
        	function getDiario() {
                var deferred = $q.defer();
                $http.get('/cuentasJson/?format=json')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });
                return deferred.promise;
            }

            function getCuentas(){
            	var deferred = $q.defer();

            	$http.get("/api/cuentas/?format=json")
            		.success(function (data){
            			deferred.resolve(data);
            		}).error(function(err){
            			deferred.resolve(err);
            		});
            	return	deferred.promise;
            }

            function getAuxiliar(){
            	var deferred = $q.defer();

            	$http("/api/auxiliar/?format=json")
            		.success(function (data){
            			deferred.resolve(data);
            		})
            		.error(function (err){
            			deferred.resolve(err);
            		});

            	return deferred.promise;
            }

            function getDiarioByFecha(FechaI, FechaF) {
            	var deferred = $q.defer();
            	
            	getDiario().then(function (data){
            		var FDesde =  FechaI.split("/");
            		var FHasta =  FechaF.split("/");

            		var desde = Date(FDesde[2], FDesde[1], FDesde[0]);
            		var hasta = Date(FHasta[2], FHasta[1], FHasta[0]);

            		var result = data.filter(fecha <= desde && fecha >= hasta);

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.reject();
            		}
            	});
            	return	deferred.promise;
            }

            function getDiarioByCuenta(FechaI, FechaF ,cuenta){
            	var deferred =$q.defer();

            	getDiarioByFecha(FechaI).then(function (data){
            		var result =data.filter(cuenta = cuenta);

            		if(result.length > 0){
            			deferred.resolve(result);
            		}else{
            			deferred.reject();
            		}
            	});
            }

            function getDiarioByAuxiliar(FechaI, FechaF, aux){
            	var deferred = $q.defer();

            	getDiario().then(function (data){
            		var result = data.filter(auxiliar = aux);

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.reject();
            		}

            	});
            }

            return {
            	getDiario:getDiario,
            	getDiarioByFecha : getDiarioByFecha,
            	getDiarioByCuenta : getDiarioByCuenta,
            	getDiarioByAuxiliar : getDiarioByAuxiliar,
            	getCuentas : getCuentas,
            	getAuxiliar : getAuxiliar

};
            }])

        .controller('ContabilidadController', ['$scope, $filter, $rootScope, ContabiliadService, $timeout', 
        					function ($scope, $filter, $rootScope, ContabiliadService, $timeout) {
        $scope.dataDiario=[];
        $scope.dataMayor = [];

        $scope.getAll = function(){
        	try{
        		$scope.dataDiario = ContabiliadService.getDiario()
        		console.log($scope.dataDiario);
        	}catch(ex){

        	}

        };

        // $scope.getCuenta = function($event){
        // 	$event.preventDefaul();

        // 	$scope.tableCuentas = true;
        // 	$scope.tableAux = false;
        // 	if($scope.suplidorNombre !== undefined) {
        //               ContabiliadService.getCuentas().then(function (data) {
        //                 $scope.cuentas = data.filter(function (registro) {
        //                    return $filter('lowercase')(registro.codigo
        //                                       .substring(0,$scope.SCuenta.length)) == $filter('lowercase')($scope.SCuenta);
        //                 });

        //                 if($scope.cuentas.length > 0){
        //                   $scope.tableCuentas = true;
        //                   $scope.cuentaNoExiste = '';
        //                 } else {
        //                   $scope.tableCuentas = false;
        //                   $scope.cuentaNoExiste = 'Esta cuenta no existe';
        //                 }

        //               });
        //             } else {
        //               ContabiliadService.getCuentas.then(function (data) {
        //                 $scope.cuentas = data;
        //                 $scope.SCuenta = '';
        //               });
        //             }

        // };
        	
        }]);
      

})(_);