
(function(_){
	angular.module('cooperativa.ahorro',['ngAnimate'])

		//=================================
		//			Services  			 ==
		//=================================

		.factory('AhorroServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/ahorrojson/';

			function getAllAhorro(){
				var deferred = $q.defer();

				$http.get(apiUrl+'?format=json&tipo=AR')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function getAllRetiros(){
				var deferred = $q.defer();

				$http.get(apiUrl+'?format=json&tipo=RT')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function getRetiroById(id){
				var deferred = $q.defer();
				getAllRetiros().then(function (data){
					var result = data.filter(function (reg){
						return reg.id == id;
					});
				});

				return deferred.promise;
			}

			function getAhorroById(id){
				var deferred =$q.defer();
				
				getAllAhorro().then(function (data){
					var result = data.filter(function (reg){
                        return reg.id==id;
					});

					if(result.length > 0){
						deferred.resolve(result);
					}
					else{
						deferred.reject();
					}
				});
				return deferred.promise;
			}

			function getAhorroSocio(socio){
				var deferred = $q.defer();

				getAllAhorro().then(function (data){
					var result = data.filter(function (reg){
						return reg.socioId == socio;
						});
					
						if(result.length > 0){
							deferred.resolve(result);
						}
						else{
							deferred.reject();
						}
					});
				 return deferred.promise;
			}

			function getRetiroSocio(socio){
				$http.get(apiUrl+'?format=json&tipo=retiro')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function setAhorroRegS(retiro){
				var deferred = $q.defer();
				
				$http.post('/ahorro/', JSON.stringify({'retiro':retiro}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (errors){
						deferred.resolve(errors);
					});
				return deferred.promise;
			}
			
			function setIntereses(fechaI, fechaF){
				var deferred = $q.defer();
				
				$http.post('/generarInteres/', JSON.stringify({'fechaI':fechaI, 'fechaF': fechaF}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (errors){
						deferred.resolve(errors);
					});
				return deferred.promise;
			}


			function generarAh(fecha, quincena){
				var deferred = $q.defer();

				$http.post('/generarAhorro/', JSON.stringify({'fecha':fecha, 'quincena': quincena}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function(err){
						deferred.resolve(err);
					});
					return deferred.promise;
			}

			function socios() {
                var deferred = $q.defer();

                $http.get('/api/socio/?format=json')
                  .success(function (data) {
                    deferred.resolve(data.filter( function(socio) {
                      return socio.estatus == "E" || socio.estatus == "S";

                    }));
                  });
                  return deferred.promise;
            }

			return {
				getAllAhorro : getAllAhorro,
				getRetiroSocio : getRetiroSocio,
				getAhorroSocio : getAhorroSocio,
				getAhorroById : getAhorroById,
				setAhorroRegS : setAhorroRegS,
				getAllRetiros : getAllRetiros,
				getRetiroById : getRetiroById,
				socios : socios,
				generarAh : generarAh,
				setIntereses : setIntereses
			};
		}])
		
	  	.controller('AhorroController', ['$scope', '$filter', '$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter, $window , $rootScope, AhorroServices, $timeout){                        	
			$scope.Ahorros=[];
			$scope.AhorrosPorSocio=[];
			$scope.AhorroHistorico=[];
			$scope.errorShow=false;
			$scope.errorMsg='';
			$scope.idAhorro=null;
			$scope.Socio=null;
			$scope.Balance=null;
			$scope.Disponible=null;
			$scope.ArrowAhorro = "UpArrow";
			$scope.ArrowDetalle = "DownArrow";
			$scope.AhorroPanel = true;
			$scope.DetalleAhorro = false;
			$scope.MaestraDetalle=[];
			$scope.tableSocio = false;
			$scope.socioReg = null;
			$scope.editer = false;
			$scope.RetiroPanel = false;
			$scope.retiro = {};
		    $scope.retiro['fecha'] = $filter('date')(Date.now(),'dd/MM/yyyy');


			$scope.getListaAhorro = function(){

			 	try{
					AhorroServices.getAllAhorro().then(function (data) {
						$scope.Ahorros=data;

					});
					
				}catch(ex){    
					$rootScope.mostrarError(ex.message);
				}
			};

			$scope.toggleAhorroPanel = function(){

				if($scope.AhorroPanel === true){
					$scope.AhorroPanel = false;
					$scope.ArrowAhorro = "DownArrow";
				}else{
					$scope.AhorroPanel = true;
					$scope.ArrowAhorro = "UpArrow";
					
				}

			}

			$scope.setAhorro = function($event){
				$event.preventDefault();
				try{
					if($scope.retiro.id === undefined){
						$scope.retiro.id = null;
					}
					var RegFecha = $scope.retiro.fecha.split('/');
          			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          			$scope.retiro.fecha = FechaFormat;
					
					var result = AhorroServices.setAhorroRegS($scope.retiro).then(function (data){
					console.log(result);
					});
					 $window.sessionStorage['retiro'] = JSON.stringify($scope.retiro);

					$scope.getListaAhorro();
					$scope.cancelRetiro();
					$scope.NoMaestra();
					$window.open('/impAhorro/', target='_blank'); 
				}

				catch(ex){
					$rootScope.mostrarError(ex.message);
				}
				
			};

			$scope.AhorroById = function(Id){
				try{

                    AhorroServices.getAhorroById(Id).then(function (data){
                    	
                    	$scope.AhorrosPorSocio = data.filter(function(reg){


                    		var salida = reg.maestra.filter(function(ret){
                    			return ret.retiro != '0';
                    		});
                    		return salida;
                    	});
                    });
                    $scope.DetalleAhorro = true;
                    $scope.toggleAhorroPanel();

                   	var xj = $scope.Ahorros.filter(function (data){
                   		return data.id==Id;
                   	});
                   	 $window.sessionStorage['ahorro'] = JSON.stringify(xj[0]);
                   	$scope.retiro['socio'] = xj[0].socioId;
                   	
					}

				catch (ex){
					$rootScope.mostrarError('Ocurrio un error al intentar cargar los datos: '+ex.message);
				}
			};

			$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   

		      };

	       	$scope.getSocio = function($event) {
	            $event.preventDefault();

	            $scope.tableSocio = true;
	            $scope.tableSuplidor = false;

	            if($scope.socioNombre !== undefined) {
	              AhorroServices.socios().then(function (data) {
	                $scope.socios = data.filter(function (registro) {
	                  return $filter('lowercase')(registro.codigo.toString()
	                                      .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
	                });

	                if($scope.socios.length == 0){
	                	$scope.socios = data.filter(function (registro) {
	                  return $filter('lowercase')(registro.nombreCompleto
	                  		.substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
	                });
	                }

	                if($scope.socios.length > 0){
	                  $scope.tableSocio = true;
	                  $scope.socioNoExiste = '';
	                } else {
	                  $scope.tableSocio = false;
	                  $scope.socioNoExiste = 'No existe el socio';
	                }

	              });
	            } else {
	              AhorroServices.socios().then(function (data) {
	                $scope.socios = data;
	                $scope.socioCodigo = '';
	              });
	            }
	          };
            
	       	$scope.postearAHorro = function(){
	       		
	       		 $scope.showPostear = true;
	       	};

	       	$scope.selSocio = function($event, s) {
	       		$event.preventDefault();

	            $scope.socioNombre = s.codigo;

	            AhorroServices.getAllAhorro().then(function (data) {
						$scope.Ahorros=data.filter(function (reg){
							return reg.socioId == s.codigo;
						});
					});

	            $scope.tableSocio = false;
	          };

	       	$scope.newRetiro = function(){
	       		$scope.RetiroPanel = true;
	       		$scope.DetalleAhorro = false;
	       	};

	       	$scope.cancelRetiro = function(){
	       		$scope.retiro =[];
	       		$scope.RetiroPanel = false;
	       		$scope.DetalleAhorro = true	;
	       	};

	       	$scope.NoMaestra = function(){
	       		$scope.AhorroPanel=true;
	       		$scope.DetalleAhorro = false;
	       	};

	       	$scope.getRegRetiro = function(id){

	       		 AhorroServices.getAllRetiros().then(function (data){
	       		 	var result = data.filter(function (reg){
	       		 		return reg.id == id;
	       		 	});
	       		 	$scope.retiro = result[0];
	       		 });
	       		 $scope.newRetiro();
	       	};
		}])
.controller('ImprimirAhorroController', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){        

			$scope.ahorro = JSON.parse($window.sessionStorage['ahorro']);
			$scope.retiro = JSON.parse($window.sessionStorage['retiro']);
			$scope.ahorroDt = {}
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			
			$scope.registro = function(){
				var balance = $scope.ahorro.balance - $scope.retiro.monto;
				var retiro = $scope.retiro.monto;
				var deuda = $scope.ahorro.balance - $scope.ahorro.disponible;
				var libre = (disponible - deuda)- retiro;


				var disponible = $scope.ahorro.disponible - $scope.retiro.monto;

				$scope.ahorroDt.socioId = $scope.ahorro.socioId;
				$scope.ahorroDt.socio = $scope.ahorro.socio;
				$scope.ahorroDt.balance = balance;
				$scope.ahorroDt.disponible = disponible;
				$scope.ahorroDt.retiro = retiro;
				$scope.ahorroDt.deuda = deuda;
				$scope.ahorroDt.libre = libre;



				var tipo;

				if ($scope.retiro.tipo == 'A'){
					tipo ="Retito de Ahorro";
				}
				else if($scope.retiro.tipo == 'J'){
					tipo = "Retiro por Ajuste";
				}
				else{
					tipo = "Retiro Otros";
				}

				$scope.retiro.tipo = tipo;

			}

			$scope.imprimir = function(){
				$window.print();
			};


		}])
.controller('ImpHistorico', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){

			$scope.AhorroDataRegistro = JSON.parse($window.sessionStorage['historico']);
			$scope.ahorroDt={}
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');


}])
.controller('GenerarAhorroCtrl', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){
			$scope.GrAhorro = [];
			$scope.quinc = [{id : 1, desc : "Quincena 1" },{id : 2, desc : "Quincena 2" }];

			$scope.generarAhorro = function(){

				var RegFecha = $scope.GrAhorro.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrAhorro.fecha = FechaFormat;

				var result = AhorroServices.generarAh($scope.GrAhorro.fecha, $scope.GrAhorro.Qui);
				console.log(result);
			};
}])

.controller('GenerarInteresCtrl', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){
			$scope.GrInteres = [];

			$scope.generarInteres = function(){

				var RegFecha = $scope.GrInteres.fechaI.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrInteres.fechaI = FechaFormat;

          	    var RegFecha2 = $scope.GrInteres.fechaF.split('/');
          		var FechaFormat2 = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrInteres.fechaF = FechaFormat2;

				var result = AhorroServices.setIntereses($scope.GrInteres.fechaI, $scope.GrInteres.fechaF);
				console.log(result)

				
			};
}]); 
})(_);