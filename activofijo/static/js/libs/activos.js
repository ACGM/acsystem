(function(_){
	angular.module('cooperativa.activofijo', ['ngAnimate'])

	.factory('ActivoServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var apiUrl='/activo/';
		
		function getActivos(){
			var deferred = $q.defer();

			$http.get(apiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});
			 return deferred.promise;
		}

		function setActivo(regActivo){
			var deferred = $q.defer();

            $http.post(apiUrl, JSON.stringify({'activo':regActivo}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		}

		function getActivosById(id){
			var deferred = $q.defer();

			getActivos.then(function (data){
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
		}

		function getSuplidor(){
                var deferred =$q.defer();

                $http.get('/api/suplidor/?format=json')
                .success(function (data){
                    deferred.resolve(data);})
                .error(function (err){
                    deferred.resource(err);
                });
                
                return deferred.promise;
        }



		return {
			getActivos 	   : getActivos,
			setActivo      : setActivo,
			getActivosById : getActivosById,
			getSuplidor    : getSuplidor
		};
	}])
	
	.controller('ActivoCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout', 
			function ($scope, $filter, $rootScope, ActivoServices, $timeout ){

			$scope.actData = [];
			$scope.lsActivos = [];
			$scope.actVs = true;
			$scope.actRg = false;

			$scope.addAct = function($event){
				$scope.actData = [];
				$scope.actVs = false;
				$scope.actRg = true;
			};

			$scope.lstActivos = function($event){
				ActivoServices.getActivos().then(function (data){
					$scope.lsActivos = data;
				})
			};

			$scope.guardarActivo = function($event){
				var result = ActivoServices.setActivo($scope.actData);
				$scope.lstActivos();
            };
		
	}])

})();