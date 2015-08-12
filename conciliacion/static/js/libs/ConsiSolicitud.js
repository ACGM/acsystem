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
	
		return {
			getSolicitudes : getSolicitudes,
			getSolicitudesById  :  getSolicitudesById,
			getSolicitudByStatus : getSolicitudByStatus
		};
	}])
	
	.controller('SolicitudChCtrl', ['$scope','$filter', '$rootScope', 'SolicitudServices','$timeout',
		function ($scope, $filter, $rootScope, SolicitudServices, $timeout) {
		$scope.lsSolicitud = [];
		$scope.solicitud = null;
		$scope.toggleCr = false;
		$scope.SolEstatus = null;

		//Lista las solicitudes realizadas.
		$scope.solicitudList = function(){
			SolicitudServices.getSolicitudes().then(function (data){
				$scope.lsSolicitud = data;
			});
		};

		//Lista las Solicitudes por estatus.
		$scope.solicitudEstatus = function($event){
			$event.preventDefault();
        	try {
				SolicitudServices.getSolicitudByStatus($scope.SolEstatus).then(function (data){
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
		}

		//Regustra una nueva solicitud.
		$scope.CrSolicitud = function($event){
			var result = SolicitudServices.setSolicitud($scope.solicitud);
			$scope.lsSolicitud = [];
			$scope.solicitudList();
		};

	}])
})();