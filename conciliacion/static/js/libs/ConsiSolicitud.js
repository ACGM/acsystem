(function(_){
	angular.module('cooperativa.solicitudCheque', ['ngAnimate'])

	.filter('estatusSolicitud', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('E', 'Cheque Emitido')
                .replace('P', 'En Proceso')
                .replace('A', 'Aprobado')
                .replace('R', 'Rechazado');
        	return input;
     	 }
  		})


	.factory('SolicitudServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var apiUrl='/conciliacion/Solicitudcheque';
		var apiRep='/conciliacion/Solicitudcheque/rg'

		function getSolicitudes(){
			var deferred = $q.defer();

			$http.get(apiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});
			 return deferred.promise;
		};

		function getSuplidor(){
                var deferred =$q.defer();

                $http.get('/api/suplidor/?format=json')
                .success(function (data){
                    deferred.resolve(data);})
                .error(function (err){
                    deferred.resource(err);
                });
                
                return deferred.promise;
        };

		function setSolicitud(solicitud){
			var deferred = $q.defer();

			$http.post(apiUrl, JSON.stringify({'solicitud':solicitud}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function getSolicitudesById(id){
			var deferred = $q.defer();

			getSolicitudes.then(function (data){
				var result = data.filter(function (reg){
					return reg.id = id;
					});

				if (result.length > 0){
					deferred.resolve(result);
				}
				else{
					deferred.reject();
				}
			});

			return deferred.promise;
		};

		function getSolicitudByStatus(estatus){
			var deferred = $q.defer();

			getSolicitudes.then(function (data){
				var result =data.filter(function (req){
					return reg.estatus = estatus;
				});

				if (result.length > 0){
					deferred.resolve(result);
				}
				else{
					deferred.reject();
				}
			});
			return deferred.promise;
		};

		function wFlow(solicitud){
			var deferred = $q.defer();

			$http.post(apiRep, JSON.stringify({'solicitud': solicitud}))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (err){
					deferred.resolve(err);
				});
			return	deferred.promise;
		};

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
			getSolicitudes : getSolicitudes,
			setSolicitud : setSolicitud,
			getSolicitudesById  :  getSolicitudesById,
			getSolicitudByStatus : getSolicitudByStatus,
			socios		 : socios,
			getSuplidor  : getSuplidor,
			wFlow        : wFlow
		};
	}])
	
	.controller('SolicitudChCtrl', ['$scope','$filter', '$rootScope', 'SolicitudServices','$timeout','$window',
		function ($scope, $filter, $rootScope, SolicitudServices, $timeout, $window) {
		$scope.lsSolicitud = [];
		$scope.socios = [];
		$scope.socioNombre = null;
		$scope.solicitud = {};
		$scope.DEstatus = null;
		$scope.tableSocio =false;
		$scope.tableSuplidor = false;
		$scope.toggleCr = false;
		$scope.toggleLs =true;
		$scope.chk = null;
		$scope.flap = false;
		$scope.btnEstatus = false;
		$scope.montoBlock = false;
		$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');


		//Lista las solicitudes realizadas.
		$scope.solicitudList = function(){
			
			SolicitudServices.getSolicitudes().then(function (data){
				$scope.lsSolicitud = data;
				console.log(data);
			});
		};

		$scope.editarSolicitud = function($event, solicitud){
			$event.preventDefault();
			if(solicitud.cxpOrden != null || solicitud.superOrden != null || solicitud.prestamo != null){
				$scope.montoBlock = true;	
			}
			
			if(solicitud.estatus != 'P'){
				$scope.btnEstatus = true;
			}

			$scope.toggleCr = true;
			$scope.toggleLs = false;
			$scope.solicitud = {};

			$scope.solicitud.id = solicitud.id;
			$scope.solicitud.socioId = solicitud.socioId;
			$scope.socioNombre = solicitud.socio;
			$scope.solicitud.suplidorId = solicitud.suplidorId;
			$scope.suplidorNombre = solicitud.suplidor;
			var temp = solicitud.fecha.split('-')

			$scope.fecha = temp[2]+'/'+temp[1]+'/'+temp[0];
			$scope.solicitud.concepto = solicitud.concepto;
			$scope.solicitud.monto = solicitud.monto;


		};

		$scope.selSocio = function($event, s) {
	   		$event.preventDefault();

	        $scope.solicitud.socioId = s.codigo;
	        $scope.socioNombre = s.nombreCompleto 

	        $scope.suplidorNombre = null;
	        $scope.solicitud.suplidorId = null;

	        $scope.tableSocio = false;
	      };


		$scope.getSuplidor = function($event){
                $event.preventDefault();
                $scope.tableSuplidor = true;
                $scope.tableSocio = false;
                if($scope.suplidorNombre != null || $scope.suplidorNombre != undefined) {
                  SolicitudServices.getSuplidor().then(function (data) {
                    $scope.suplidor = data.filter(function (registro) {
                       return $filter('lowercase')(registro.nombre
                                          .substring(0,$scope.suplidorNombre.length)) == $filter('lowercase')($scope.suplidorNombre);
                    });

                    if($scope.suplidor.length > 0){
                      $scope.tableSuplidor = true;
                      $scope.suplidorNoExiste = '';
                    } else {
                      $scope.tableSuplidor = false;
                      $scope.suplidorNoExiste = 'No existe el suplidor';
                    }

                  });
                } else {
                  SolicitudServices.getSuplidor().then(function (data) {
                    $scope.suplidor = data;
                    $scope.suplidorCodigo = '';
                  });
                }
              };


        $scope.selSuplidor = function($event, s) {
	        $event.preventDefault();
	        $scope.suplidorNombre = s.nombre;
	        $scope.solicitud.suplidorId = s.id;

	         $scope.solicitud.socioId = null;
	        $scope.socioNombre = null;

	        $scope.tableSuplidor= false;
	      };

		//Lista las Solicitudes por estatus.
		$scope.solicitudEstatus = function($event){
			$event.preventDefault();
			alert($scope.DEstatus);
			
        	try {
        		
				//SolicitudServices.getSolicitudByStatus(estatus).then(function (data){
				//	$scope.lsSolicitud = data;
				//});
			}
			 catch (e) {
	          notie.alert(3,e,4);
	        }
			};

		//Trae todo el detalle de una solicitud.
		$scope.SolicitudId = function(id){
			SolicitudServices.getSolicitudesById(id).then(function (data){
				$scope.solicitud = data;
			});
			};


		$scope.setSolicitud = function($event){
			$event.preventDefault();
			try{

				var RegFecha = $scope.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          		$scope.solicitud.fecha = FechaFormat;
				
				if($scope.solicitud.id == undefined){
					$scope.solicitud.id = null;
					$scope.solicitud.estatus = 'P';
				};
				
				if($scope.solicitud.socioId == undefined){
					$scope.solicitud.socioId = null;
				};

				if($scope.solicitud.suplidorId == undefined){
					$scope.solicitud.suplidorId = null;
				};

				if($scope.solicitud.id == undefined){
					$scope.solicitud.id = null;

					SolicitudServices.setSolicitud($scope.solicitud).then(function (data){
					
					if(data=="Ok"){
						notie.alert(1 , "Solicitud Creada",2.5);
						 $scope.limpiar();
						$scope.solicitudList();
					}else{
						notie.alert(3 ,"Ha ocurrido un error, No fue posible Crear la solicitud", 3);
						console.log(data);
					}
					});
				}
				else{
					SolicitudServices.setSolicitud($scope.solicitud).then(function (data){
					
					if(data=="Ok"){
						notie.alert(1 , "Fueron realizados los cambios de manera exitosa.",3);
						 $scope.limpiar();
						$scope.solicitudList();
					}else{
						notie.alert(3 ,"Ha ocurrido un error, No fue posible actualizar la solicitud", 3);
						console.log(data);
					}
				}
				);
				}
			
			}
			catch(e){
				notie.alert(3,e,5);			}
			};


		$scope.workflow = function($event,id){
			$event.preventDefault();
			$scope.chk = id;
			$scope.flap = true;
		};

		$scope.cancelarSolicitud = function($event){
			$scope.toggleCr = false;
			$scope.toggleLs = true;
			$scope.solicitud = {};
		};

		$scope.nwRegistro = function($event){
			$scope.toggleCr = true;
			$scope.toggleLs = false;
			$scope.solicitud = {};
		};

		$scope.ActEstatus = function($event,estatus){
			$event.preventDefault();
			var est = null;
			if(estatus == "aceptado"){
				est = "A";
			}
			else if( estatus == "cancelado") {
				est = "R";
			};

			if(est != null){
				var sol = {};
				sol.solId = $scope.chk;
				sol.estatus = est;
				console.log(sol);
				SolicitudServices.wFlow(sol).then(function (data){
					if(data == "Ok"){
						$scope.flap = false;
						notie.alert(1,"Se ha completado la solicitud #"+$scope.chk, 2.5);
						$scope.chk = null;
						$scope.limpiar();
					}
					else{
						$scope.flap = false;
						notie.alert(3,"Ocurrio un error al intentar aprobar.", 3);
						console.log(data);
						$scope.limpiar();
					}
				});
				$scope.solicitudList();

			};
			$scope.solicitudList();	

		};

		$scope.printSol = function($event,id){
			var data = $scope.lsSolicitud .filter(function (reg){
				return reg.id == id;
			});
			
			console.log(data);
			$window.sessionStorage['solicitud'] = JSON.stringify(data);

	       	$window.open('/conciliacion/Solicitudcheque/rg', target='_blank'); 
		};

		//Registra una nueva solicitud.	
		$scope.CrSolicitud = function($event){
			$event.preventDefault();
			
			try {
				var result = SolicitudServices.setSolicitud($scope.solicitud);
				$scope.limpiar();
			}
			 catch (e) {
	          notie.alert(3,e,4);
	        }
			};


		$scope.getSocio = function($event) {
	            $event.preventDefault();

	            $scope.tableSocio = true;

	            if($scope.socioNombre) {
	              SolicitudServices.socios().then(function (data) {
	                $scope.socios = data.filter(function (registro) {
	                	console.log(registro);
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
	              SolicitudServices.socios().then(function (data) {
	                $scope.socios = data;
	                $scope.socioCodigo = '';
	              });
	            }
	          };


	    $scope.limpiar = function($event){
	    	$scope.lsSolicitud = [];
			$scope.socios = [];
			$scope.socioNombre = null;
			$scope.solicitud = {};
			$scope.DEstatus = null;
			$scope.tableSocio =false;
			$scope.tableSuplidor = false;
			$scope.toggleCr = false;
			$scope.toggleLs =true;
			$scope.chk = null;
			$scope.flap = false;
			$scope.btnEstatus = false;
			$scope.montoBlock = false;
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			$scope.solicitudList();

	    }
	}])
	.controller('SolicitudImpCtrl',['$scope','$filter', '$rootScope','SolicitudServices','$timeout','$window',
		function ($scope, $filter,$rootScope,$SolicitudServices,$timeout,$window){

			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			$scope.loadAll = function(){
				$scope.regData = JSON.parse($window.sessionStorage['solicitud']);	
				console.log($scope.regData[0]);			
			}
		}]);
})();