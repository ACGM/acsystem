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
		}
	
		return {
	
		};
	}])
})();