(function(_){
	angular.module('cooperativa.chequeConc', ['ngAnimate'])

	.factory('ChequesServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var SolicitudApiUrl='/conciliacion/Solicitudcheque/';
		var apiUrl='/conciliacion/Cheques';

		function getCheques(){
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

		function setCheques(cheque){
			var deferred = $q.defer();

			http.post(apiUrl, JSON.stringify({'cheque':cheque}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function getChequeById(id){
			var deferred = $q.defer();

			getCheques().then(function (data){
				var result= data.filter(function (reg){
					return reg.id = id; 
				});

				if(result.length > 0){
					deferred.resolve(result);
				}else{
					deferred.reject();
				}

				return deferred.response;
			});
		};

		function getSolicitudes(){
			var defered = $q.defer();

			$http.get(SolicitudApiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
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

		return {
			getCheques : getCheques,
			setCheques : setCheques,
			getSolicitudes : getSolicitudes,
			getSolicitudByStatus : getSolicitudByStatus,
			getSolicitudesById : getSolicitudesById,
			getChequeById : getChequeById
		};
	}])

	.controller('ChequeCtrl', ['$scope','$filter', '$rootScope', 'ChequesServices','$timeout', 
		function ($scope, $filter, $rootScope, ChequesServices, $timeout) {
		$scope.LsSolicitud = [];
		$scope.Solicitud = null;
		$scope.reCheque = null;
		$scope.ToggleCh = true;

		$scope.getSolicitudes = function($event){
			getSolicitudByStatus('P').then(function (data){
				$scope.LsSolicitud = data;
			});
		};

		$scope.setConCheque = function($event){
				try{
					ChequesServices.setCheques($scope.reCheque).then(function (data){
						var resp = data;
					});
				}
				catch(e){
					$rootScope.mostrarError(e);
				}
			}

		$scope.getSolicitud = function($event, id){
			$event.preventDefault();

			getSolicitudesById(id).then(function (data){
				$scope.Solicitud = data;
			});
		};

		$scope.getCheque = function($evnet, id){
			$event.preventDefault();
			$scope.reCheque = null;

			ChequesServices.getChequeById(id).then(function (data){
				$scope.reCheque = data;
			});
		};

		$scope.insCheque = function($event){
			$event.preventDefault();

			try{
				var result = ChequesServices.setCheques($scope.reCheque);
			}
			 catch (e) {
	          $rootScope.mostrarError(e);
	        }
		};
		
	}]);
})();