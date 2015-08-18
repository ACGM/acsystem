(function(_){
	angular.module('cooperativa.solicitudCheque', ['ngAnimate'])

	.factory('SolicitudServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var apiUrl='/conciliacion/Solicitudcheque/';

		function getSolicitudes(){
			var defered = $q.defer();

			$http.get(apiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});
			 return deferred.promise;
		};

		function setSolicitud(solicitud){
			var deferred = $q.defer();

			http.post(apiUrl, JSON.stringify({'solicitud':solicitud}))
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
			socios		 : socios
		};
	}])
	
	.controller('SolicitudChCtrl', ['$scope','$filter', '$rootScope', 'SolicitudServices','$timeout',
		function ($scope, $filter, $rootScope, SolicitudServices, $timeout) {
		$scope.lsSolicitud = [];
		$scope.socios = [];
		$scope.solicitud = null;
		$scope.tableSocio =false;
		$scope.toggleCr = false;
		$scope.toggleLs =true;


		//Lista las solicitudes realizadas.
		$scope.solicitudList = function(){
			SolicitudServices.getSolicitudes().then(function (data){
				$scope.lsSolicitud = data;
			});
		};

		$scope.selSocio = function($event, s) {
	   		$event.preventDefault();

	        $scope.solicitud.socioId = s.codigo;
	        $scope.solicitud.socio = s.nombreCompleto 

	        $scope.tableSocio = false;
	      };


		//Lista las Solicitudes por estatus.
		$scope.solicitudEstatus = function($event, estatus){
			$event.preventDefault();
        	try {
				SolicitudServices.getSolicitudByStatus(estatus).then(function (data){
					$scope.lsSolicitud = data;
				});
			}
			 catch (e) {
	          $rootScope.mostrarError(e);
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
				SolicitudServices.setSolicitud($scope.solicitud).then(function (data){
					var resp = data;
				});
			}
			catch(e){
				$rootScope.mostrarError(e);
			}
		};

		//Registra una nueva solicitud.
		$scope.CrSolicitud = function($event){
			$event.preventDefault();
			
			try {
				var result = SolicitudServices.setSolicitud($scope.solicitud);
				$scope.lsSolicitud = [];
				$scope.solicitudList();
			}
			 catch (e) {
	          $rootScope.mostrarError(e);
	        }
		};

		$scope.cancelarSolicitud = function($event){
			$event.preventDefault();
			
			$scope.solicitud = null;
			$scope.tableSocio =false;
			$scope.toggleCr = false;
			$scope.toggleLs =true;

			$scope.solicitudList();

		}

		$scope.getSocio = function($event) {
	            $event.preventDefault();

	            $scope.tableSocio = true;

	            if($scope.solicitud.socio !== undefined) {
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

	}]);
})();