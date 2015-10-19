(function(_){
	angular.module('cooperativa.chequeConc', ['ngAnimate'])

	.factory('ChequesServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var SolicitudApiUrl='/conciliacion/Solicitudcheque';
		var apiUrl='/conciliacion/Cheques';

		function getCheques(){
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

		function setCheques(cheque){
			var deferred = $q.defer();

			$http.post(apiUrl, JSON.stringify({'cheque':cheque}))
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
			var deferred = $q.defer();

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

			getSolicitudes().then(function (data){
				var result =data.filter(function (reg){
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

			getSolicitudes().then(function (data){
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

	.controller('ChequeCtrl', ['$scope','$filter', '$rootScope', 'ChequesServices','$timeout', '$window',
		function ($scope, $filter, $rootScope, ChequesServices, $timeout, $window) {
		$scope.LsSolicitud = [];
		
		$scope.Solicitud = {};
		$scope.LsCheques = [];

		$scope.reCheque = {};

		$scope.ToggleCh = false;
		$scope.ToggleSl = false;
		$scope.ToggleNCh = false;

		$scope.listSolicitud = function($event){
			$event.preventDefault();

			$scope.ToggleSl = true;
			$scope.ToggleNCh = false;
			$scope.ToggleCh = false;
			ChequesServices.getSolicitudByStatus('A').then(function (data){
				$scope.LsSolicitud = data;
			});

		};

		$scope.NewCheque =function($event,s){
			$event.preventDefault();

			$scope.reCheque.solicitud = s.id
			var fecha = s.fecha.split('-')
			$scope.reCheque.id = null;
			$scope.reCheque.fecha = fecha[2]+"/"+fecha[1]+"/"+fecha[0];
			$scope.reCheque.estatus = "R";
			if(s.socio != undefined){
				$scope.reCheque.beneficiario = s.socio	
			}
			else{
				$scope.reCheque.beneficiario = s.supervisor
			};

			$scope.ToggleCh = false;
			$scope.ToggleSl = false;
			$scope.ToggleNCh = true;
		}

		$scope.listCheques = function($event){
			$event.preventDefault();

			$scope.ToggleSl = false;
			$scope.ToggleNCh = false;
			$scope.ToggleCh = true;

			ChequesServices.getCheques().then(function (data){
				$scope.LsCheques = data;
			});

		};

		$scope.getSolicitudes = function($event){
			ChequesServices.getSolicitudByStatus('P').then(function (data){
				$scope.LsSolicitud = data;

			});
		};

		$scope.setConCheque = function($event){
			$event.preventDefault();
			try{
				var RegFecha = $scope.reCheque.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          		$scope.reCheque.fecha = FechaFormat;

				ChequesServices.setCheques($scope.reCheque).then(function (data){
					var resp = data;
				});
			}
			catch(e){
				$rootScope.mostrarError(e);
			}
			}

		$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		    };


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
				var result = ChequesServices.setCheques($scope.reCheque).then(function (data){
					if(data == "Ok"){
						$scope.cancelRegistro();
					}else{
						$rootScope.mostrarError("Ha ocurrido un error al guardar cheque");
					}
				} );
			}
			 catch (e) {
	          $rootScope.mostrarError(e);
	        }
		};

		$scope.printChk = function($event,ch){
			$window.sessionStorage['chk'] = JSON.stringify(ch);

			$window.open('/conciliacion/Cheques/im', target='_blank'); 
		};

		$scope.cancelRegistro = function($event){
			$scope.ToggleCh = false;
			$scope.ToggleSl = true;
			$scope.ToggleNCh = false;
		};
		
	}])

	.controller('ImpchequeCtrl', ['$scope','$filter', '$rootScope', 'ChequesServices','$timeout', '$window' ,
		function ($scope, $filter, $rootScope, ChequesServices, $timeout, $window) {

			$scope.dia =null;
			$scope.mes =null;
			$scope.agno =null;

			$scope.nombre = null;
			$scope.monto = null;
			$scope.letras =null;
			$scope.fecha = null;
			$scope.concepto = null;
			$scope.cuentas = [];

		$scope.start = function(){
			debugger;
			$scope.regData = JSON.parse($window.sessionStorage['chk']);
			$scope.cuentas = $scope.regData.cuenta;
			var formFecha = $scope.regData.fecha.split('-');
			$scope.dia = formFecha[2];
			$scope.mes = formFecha[1];
			$scope.agno = formFecha[0];


			
		}	
			
	}]);
})();