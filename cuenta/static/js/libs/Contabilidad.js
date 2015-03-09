(function(_){
	 angular.module('cooperativa.contabilidad',['ngAnimate'])

        .factory('ContabilidadService', ['$http','$q','$filter', function ($http, $q, $filter) {
        	 
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

            function getCuentasReg(){
            	var deferred = $q.defer();

            	$http.get('/api/cuentas/?format=json')
            		.success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });
                 return deferred.promise;
            }

            function getAuxiliar(){
            	var deferred = $q.defer();

                $http.get('/api/auxiliar/?format=json')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });
                 return deferred.promise;
            }

            function getDiarioByFecha(FechaI, FechaF) {
            	var deferred = $q.defer();
            	
            	getDiario().then(function (data){
            		var FDesde =  FechaI.split("/");
            		var FHasta =  FechaF.split("/");

            		var result = data.filter(function (reg){
                           
                        return new Date(reg.fecha.split("-")[0],parseInt(reg.fecha.split("-")[1])-1,reg.fecha.split("-")[2]) 
                            >= new Date(FDesde[2], parseInt(FDesde[1])-1, FDesde[0]) 
                            &&  new  Date(reg.fecha.split("-")[0],parseInt(reg.fecha.split("-")[1])-1,reg.fecha.split("-")[2]) 
                            <= new Date(FHasta[2], parseInt(FHasta[1])-1, FHasta[0])
                        
                    });
                    
          

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.resolve(result);
            		}
            	});
            	return	deferred.promise;
            }

            function getDiarioByCuenta(FechaI, FechaF, cuenta){
            	var deferred = $q.defer();
              
            	getDiarioByFecha(FechaI, FechaF).then(function (data){
            		var result = data.filter(function (reg){
                        console.log(reg.cuenta == cuenta);
                        return reg.cuenta == cuenta; 
                    });
            		if(result.length > 0){
            			deferred.resolve(result);
            		}else{
            			deferred.reject();
            		}
            	});
                return deferred.promise;
            }

            function getDiarioByAuxiliar(FechaI, FechaF, aux){
            	var deferred = $q.defer();

            	getDiario().then(function (data){
            		var result = data.filter(function (reg){
                        return reg.auxiliar == aux;
                    });

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.reject();
            		}
                    console.log(result);

            	});
                  return deferred.promise;

            }

            return {
            	getDiario : getDiario,
            	getDiarioByFecha : getDiarioByFecha,
            	getDiarioByCuenta : getDiarioByCuenta,
            	getDiarioByAuxiliar : getDiarioByAuxiliar,
            	getCuentasReg : getCuentasReg,
            	getAuxiliar : getAuxiliar

				};
            }])

        .controller('ContabilidadController', ['$scope','$filter', '$rootScope', 'ContabilidadService','$timeout', 
        					function ($scope, $filter, $rootScope, ContabilidadService, $timeout) {
        var date = new Date();

        $scope.diario = [];
        $scope.dataMayor = [];
        $scope.cuenta = null;
        $scope.aux = null;
        $scope.cuentas = null;
        $scope.SFechaI = $filter('date')(new Date(date.getFullYear(), date.getMonth(),1),'dd/MM/yyyy');
        $scope.SFechaF = $filter('date')(new Date(date.getFullYear(), date.getMonth(),28),'dd/MM/yyyy');
        $scope.totalCredito = 0;
        $scope.totalDebito = 0;
        $scope.panelTotal ="total-compensado"

        $scope.getAll = function(data){
            ContabilidadService.getDiario().then(function (data){
                 $scope.diario = data;
                 $scope.calTotales();
            });
              
        };

        $scope.getByDate = function(){
        	try{

        		  ContabilidadService.getDiarioByFecha($scope.SFechaI, $scope.SFechaF).then(function (data){
                    if(data.length > 0){
                        $scope.diario = data;
                        $scope.calTotales();
                    }else{
                        $scope.diario=[];
                        $scope.calTotales();
                    }
                  });
        	}catch(ex){
                    $scope.diario=[];
                    $scope.calTotales();
        	}

        };
        $scope.Clear = function(){

             $scope.SFechaI = $filter('date')(new Date(date.getFullYear(), date.getMonth(),1),'dd/MM/yyyy');
             $scope.SFechaF = $filter('date')(new Date(date.getFullYear(), date.getMonth(),28),'dd/MM/yyyy');
             $scope.SAux = null;
             $scope.SCuenta = null;
             $scope.FillResult();
        };

        $scope.getByAux = function(){
            try{
                ContabilidadService.getDiarioByAuxiliar($scope.SFechaI, $scope.SFechaF, $scope.SAux).then(function (data){
                   if(data.length > 0) {
                        $scope.diario = data;
                        $scope.calTotales();
                    }else{
                        $scope.diario=[];
                        $scope.calTotales();
                    }
                });
            }
            catch(ex){
                $scope.diario = [];
                $scope.calTotales();
                console.log(ex);
            }
        };

        $scope.getByCuenta = function (){
            try{
                ContabilidadService.getDiarioByCuenta($scope.SFechaI, $scope.SFechaF, $scope.SCuenta).then(function (data){
                   if(data.length > 0){
                        $scope.diario = data;
                        $scope.calTotales();
                   }else{
                        $scope.diario = data;
                        $scope.calTotales();
                   }
                    
                });
            }
            catch(ex){
                $scope.diario =[];
                $scope.calTotales();
                console.log(ex);
            }
        };

        $scope.FillResult = function(){
            if($scope.SCuenta != undefined){
                 $scope.getByCuenta();
             }else if($scope.SAux != undefined){
                 $scope.getByAux(); 
             }else {
                 $scope.getByDate();
             }

            $scope.calTotales();
        }

        $scope.getCuenta = function($event){
        	$event.preventDefault();
        	
        	$scope.tableCuentas = true;
        	$scope.tableAux = false;
        	if($scope.SCuenta !== undefined) {
                ContabilidadService.getCuentasReg().then(function (data){
                    $scope.cuentas = data.filter(function (reg){
                        return reg.codigo.toString().substring(0,$scope.SCuenta.length) == $scope.SCuenta;
                    });
                    if($scope.cuentas.length >0){
                        $scope.tableCuentas = true;
                        $scope.cuentaNoExiste = "";
                    }else{
                        $scope.tableCuentas = false;
                        $scope.cuentaNoExiste = "No existe esta cuenta";
                    }
                });
            } else {
               ContabilidadService.getCuentasReg().then(function (data){	
                $scope.cuentas = data;
                $scope.cuentaNoExiste = ''; 

              });
            }

        };

        $scope.calTotales = function(){
            $scope.totalDebito = 0;
            $scope.totalCredito = 0;
            if($scope.diario.length>0){

                for (x = 0; x < $scope.diario.length; x ++){
                    $scope.totalDebito = $scope.totalDebito + parseFloat($scope.diario[x].debito);
                    $scope.totalCredito = $scope.totalCredito + parseFloat($scope.diario[x].credito);
                }
                if(parseFloat($scope.totalCredito) == parseFloat($scope.totalDebito)){
                    $scope.panelTotal ="total-compensado"
                }else{
                    $scope.panelTotal ="total-noCompensado"
                }
            }
        }

        $scope.getAux = function($event){
            $event.preventDefault();
            
            $scope.tableCuentas = false;
            $scope.tableAux = true;
            if($scope.SAux !== undefined) {
                ContabilidadService.getAuxiliar().then(function (data){
                    $scope.aux = data.filter(function (reg){
                        return reg.codigo.toString().substring(0,$scope.SAux.length) == $scope.SAux;
                    });
                    if($scope.aux.length >0){
                        $scope.tableCuentas = true;
                        $scope.cuentaNoExiste = "";
                    }else{
                        $scope.tableCuentas = false;
                        $scope.auxNoExiste = "No existe esta cuenta";
                    }
                });
            } else {
               ContabilidadService.getAuxiliar().then(function (data){    
                $scope.aux = data;
                $scope.SCueauxNoExistenta = ''; 
              });
            }

        };

        $scope.selCuenta = function($event, s) {
                $event.preventDefault();
                $scope.SCuenta = s.codigo;
                $scope.tableCuentas = false;
              };


        $scope.selAux = function($event, s) {
                $event.preventDefault();
                $scope.SAux = s.codigo;
                $scope.tableAux = false;
              };
        	
        }]
        );

})(_);