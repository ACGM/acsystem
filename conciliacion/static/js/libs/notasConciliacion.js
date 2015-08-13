(function (_){
	angular.module('cooperativa.notaConc', ['ngAnimate'])

	.factory('NotasConcServices', ['$http','$q','$filter', 
		function ($http, $q, $filter) {
			var apiUrl='/conciliacion/notas';
			var NostasApiUrl='/conciliacion/notas/rg/';

			function getNotas(){
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

			function setNotas(notas){
				var deferred = $q.defer();

				http.post(apiUrl, JSON.stringify({'Notas':notas}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};

			function getNotasId(id){
				var deferred = $q.defer();

				getNotas().then(function (data){
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

			function getNotasByType(tipo){
				var deferred = $q.defer();

				getNotas().then(function (data){
					var result= data.filter(function (reg){
						return reg.tipo = tipo; 
					});

					if(result.length > 0){
						deferred.resolve(result);
					}else{
						deferred.reject();
					}

					return deferred.response;
				});
			};
			
			function getNotasByFecha(fechaI, fechaf){
				var deferred = $q.defer();

				$http.get(NostasApiUrl+'?fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});

				return deferred.promise;
			}
	
		return {
			getNotas : getNotas,
			setNotas : setNotas,
			getNotasId : getNotasId,
			getNotasByType : getNotasByType,
			getNotasByFecha, getNotasByFecha


		};
	}])
	
	.controller('NotasConcCtrl', ['$scope','$filter', '$rootScope', 'NotasConcServices','$timeout', 
		function ($scope, $filter, $rootScope, NotasConcServices, timeout ) {
			$scope.LsNotas = [];
			$scope.Nota = null;

			$scope.getConcNotas = function($event){
				NotasConcServices.getNotas().then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

			$scope.setConNotas = function($event){
				try{
					NotasConcServices.setNotas($scope.Nota).then(function (data){
						var resp = data;
					});
				}
				catch(e){
					$rootScope.mostrarError(e);
				}
			}

			$scope.getConNota = function($event, id){
				NotasConcServices.getNotasId(id).then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

			$scope.getConNotaType = function($event, tipo){
				NotasConcServices.getNotasByType(tipo).then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

			$scope.getConNotaFecha = function($event, fechaI, fechaF){
				NotasConcServices.getNotasByFecha(fechai, fechaF).then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

	}]);
})();