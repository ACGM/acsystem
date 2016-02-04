(function(_){
	angular.module('cooperativa.conciliacionBanco', ['ngAnimate'])

	.factory('conciliacionServices', ['$http','$q','$filter', function ($http, $q, $filter) {
		var apiUrl='/conciliacion/banco';
		var apiUrl2='/conciliacion/banco/rg';
		var depositoApi='/conciliacion/depositos';
		var chkTransApi ='/conciliacion/chkTrans';
		var repConc = -'/conciliacion/registros';

		function getDeposito(){
			var deferred = $q.defer();

			$http.get(depositoApi+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})

				.error(function (error){
					deferred.resolve(error);
				});

			 return deferred.promise;
			};


		function setDeposito(deposito){
				var deferred = $q.defer();
			
				$http.post(depositoApi, JSON.stringify({'deposito':deposito}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};


		function getDepositoFecha(fechaI, fechaF){
			var deferred = $q.defer();

			$http.get('/conciliacion/deposito/rg?format=json&fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});

			return deferred.promise;
		};


		function getChkTrnasito(){
			var deferred = $q.defer();

			$http.get(chkTransApi+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})

				.error(function (error){
					deferred.resolve(error);
				});

			 return deferred.promise;
			};


		function setChkTransito(ChkTransito){
				var deferred = $q.defer();
			
				$http.post(chkTransApi, JSON.stringify({'ChkTransito':ChkTransito}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};


		function getChkTransitoFecha(fechaI, fechaF){
			var deferred = $q.defer();

			$http.get('/conciliacion/chkTrans/rg?format=json&fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});

			return deferred.promise;
		};


		function getBanco(){
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


		function setBanco(banco){
				var deferred = $q.defer();
			
				$http.post(apiUrl, JSON.stringify({'banco':banco}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};


		function getBancoById(id){
			var deferred = $q.defer();

			getBanco().then(function (data){
				var result= data.filter(function (reg){
					return reg.id = id; 
				});

				if(result.length > 0){
					deferred.resolve(result);
				}else{
					deferred.reject();
				}
			});

			return deferred.response;
		};


		function getBancoByType(tipo){
			var deferred = $q.defer();

			getBanco().then(function (data){
				var result= data.filter(function (reg){
					return reg.tipo = tipo; 
				});

				if(result.length > 0){
					deferred.resolve(result);
				}else{
					deferred.reject();
				}

			});

			return deferred.response;
		}


		function getBancoFecha(fechaI, fechaF){
			var deferred = $q.defer();

			$http.get(apiUrl2+'?format=json&fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});

			return deferred.promise;
		};

		function getConcRep(fechaI, fechaF){
			var deferred = $q.defer();

			$http.get(repConc+'?format=json&fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}', fechaI).replace('{fechaF}',fechaF))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (err){
					deferred.resolve(err);
				});

			return deferred.promise;
		};

		return {
			getBanco : getBanco,
			setBanco : setBanco,
			getDeposito : getDeposito,
			setDeposito : setDeposito,
			getDepositoFecha : getDepositoFecha,
			getChkTrnasito : getChkTrnasito,
			setChkTransito : setChkTransito,
			getChkTransitoFecha : getChkTransitoFecha,
			getBancoById : getBancoById,
			getBancoByType : getBancoByType,
			getBancoFecha : getBancoFecha,
			getConcRep	: getConcRep

		};
	}])
	
	.controller('ConciliacionCtrl', ['$scope','$filter', '$rootScope', 'conciliacionServices','$timeout', '$window', 
		function ($scope, $filter, $rootScope, conciliacionServices, $timeout, $window) {
		
		$scope.bancoLs = [];
		$scope.regBanco = {};
		$scope.fechai = null;
		$scope.fechaf = null;
		$scope.toggleBanco = false;
		$scope.NwBanco = false;
		$scope.LsBanco = true;

		$scope.getBancoList = function(){
			$scope.regBanco = {};
			conciliacionServices.getBanco().then(function (data){
				$scope.bancoLs = data;
			});
		};

		$scope.nwRegistro = function($event){
			$scope.NwBanco = true;
			$scope.LsBanco = false;
		};

		$scope.cancelarReg = function($event){
			$event.preventDefault();
			$scope.regBanco = {};
			$scope.NwBanco = false;
			$scope.LsBanco = true;
			$scope.getBancoList();
		};

		$scope.impBanco = function($event){
			$event.preventDefault();
			$scope.datosR = null;
			$scope.datosT = null;
			$scope.datosC = null;

			$scope.cabeceraR = {tipo: 'Banco',
								titulo: 'registrado'};

			$scope.cabeceraT = {tipo: 'Banco',
								titulo: 'en Transito'};

			$scope.cabeceraC = {tipo: 'Banco',
								titulo: 'Cerrado'};

			$scope.datosR = $scope.bancoLs.filter(function (data){
				return data.estatus == 'R'
				});

			$scope.datosT = $scope.bancoLs.filter(function (data){
				return data.estatus == 'T'
				});

			$scope.datosC = $scope.bancoLs.filter(function (data){
				return  data.estatus == 'C'
				});

			$scope.imprimirReporte($scope.datosR, $scope.cabeceraR);
			$scope.imprimirReporte($scope.datosT, $scope.cabeceraT);
			$scope.imprimirReporte($scope.datosC, $scope.cabeceraC);

		}


		$scope.imprimirReporte = function(datos, cabecera){
				if (datos.length > 0){
					$window.sessionStorage['concCabecera'] = JSON.stringify(cabecera);
					$window.sessionStorage['concGenerico'] = JSON.stringify(datos);
					$window.open('/conciliacion/salida', target='_blank'); 
				}
			};


		$scope.editReg = function(id){
			var reg = $scope.bancoLs.filter(function(data){
				return data.id == id;
			})
			console.log(reg[0]);
			$scope.regBanco.id = reg[0].id;
			$scope.regBanco.fecha = reg[0].fecha;

			var RegFecha = reg[0].fecha.split('-');
      		var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
      		$scope.regBanco.fecha= FechaFormat;

			$scope.regBanco.descripcion = reg[0].descripcion;
			$scope.regBanco.tipo = reg[0].tipo;
			$scope.regBanco.estatus = reg[0].estatus;
			$scope.regBanco.monto = reg[0].monto;

			$scope.nwRegistro();

		}

		$scope.getBancoFecha = function(){
			
			var regFechaI = $scope.fechai.split('/');
			var formt1 = regFechaI[2] + '-' + regFechaI[1] + '-' + regFechaI[0]; 

			var regFechaF = $scope.fechaf.split('/');
			var formt2 = regFechaF[2] + '-' + regFechaF[1] + '-' + regFechaF[0]; 

			conciliacionServices.getBancoFecha(formt1, formt2).then(function (data){
				$scope.bancoLs = data;
				});
			
		};

		$scope.setConBanco = function($event){
			$event.preventDefault();
			try{
				
				if($scope.regBanco.id === undefined){
					$scope.regBanco.id = null;
				}

				var RegFecha = $scope.regBanco.fecha.split('/');
      			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
      			$scope.regBanco.fecha = FechaFormat;

				console.log($scope.regBanco);
				conciliacionServices.setBanco($scope.regBanco).then(function (data){
					var resp = data;
					if (resp == "Ok"){
						notie.alert(1,"Registro almacenado de forma exitosa", 3);
					}else{
						notie.alert(3,"Ocurrio un error al realizar el registro",4);
						console.log(resp);
					}
				});
				
				$scope.cancelarReg($event);
			}
			catch(e){
				notie.alert(3,"Ocurrio un error interno en la aplicacion", 4);
				console.log(e);
			}
		};

		$scope.getBancoListType = function(tipo){
			conciliacionServices.getBancoByType(tipo).then(function (data){
				$scope.bancoLs = data;
			});
		};

		$scope.getBancoId = function(id){
			conciliacionServices.getBancoId(id).then(function (data){
				$scope.banco = data;
			});
		};

		$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		    };
	}])

	.controller('ChkTansitoCtrl', ['$scope','$filter', '$rootScope', 'conciliacionServices','$timeout', '$window', 
		function ($scope, $filter, $rootScope, conciliacionServices, $timeout, $window) {
			$scope.ChkTransitoLs = [];
			$scope.regChkTrans = {};
			$scope.fechai = null;
			$scope.fechaf = null;
			$scope.NwChkTran = false;
			$scope.LschkTransito = true;

			$scope.getchkTransitoFecha = function(){
				
				var regFechaI = $scope.fechai.split('/');
				var formt1 = regFechaI[2] + '-' + regFechaI[1] + '-' + regFechaI[0]; 

				var regFechaF = $scope.fechaf.split('/');
				var formt2 = regFechaF[2] + '-' + regFechaF[1] + '-' + regFechaF[0]; 

				conciliacionServices.getChkTransitoFecha(formt1, formt2).then(function (data){
						$scope.ChkTransitoLs = data;
				
				});
			};

			$scope.geChkTransitoList = function(){
				
				$scope.regChkTrans = {};
				conciliacionServices.getChkTrnasito().then(function (data){
					$scope.ChkTransitoLs = data;
			});

			$scope.nwRegistro = function(){
				
				$scope.NwChkTran = true;
				$scope.LschkTransito = false;
				
			};

			$scope.impChkTrans = function($event){
				$event.preventDefault();
				$scope.datosR = null;
				$scope.datosT = null;
				$scope.datosC = null;

				$scope.cabeceraR = {tipo: 'Cheque en transito',
									titulo: 'registrado'};

				$scope.cabeceraT = {tipo: 'Cheque en transito',
									titulo: 'en Transito'};

				$scope.cabeceraC = {tipo: 'Cheque en transito',
									titulo: 'Cerrado'};

				$scope.datosR = $scope.ChkTransitoLs.filter(function (data){
					return data.estatus == 'R'
					});

				$scope.datosT = $scope.ChkTransitoLs.filter(function (data){
					return data.estatus == 'T'
					});

				$scope.datosC = $scope.ChkTransitoLs.filter(function (data){
					return  data.estatus == 'C'
					});
				
				$scope.imprimirReporte($scope.datosR, $scope.cabeceraR);
				$scope.imprimirReporte($scope.datosT, $scope.cabeceraT);
				$scope.imprimirReporte($scope.datosC, $scope.cabeceraC);


			}


			$scope.imprimirReporte = function(datos, cabecera){
					if (datos.length > 0){
						$window.sessionStorage['concCabecera'] = JSON.stringify(cabecera);
						$window.sessionStorage['concGenerico'] = JSON.stringify(datos);
						$window.open('/conciliacion/salida', target='_blank'); 
					}
				};

			$scope.editReg = function(id){
				var reg = $scope.ChkTransitoLs.filter(function(data){
					return data.id == id;
				})
				console.log(reg[0]);
				$scope.regChkTrans.id = reg[0].id;
				$scope.regChkTrans.fecha = reg[0].fecha;

				var RegFecha = reg[0].fecha.split('-');
	      		var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
	      		$scope.regChkTrans.fecha= FechaFormat;

				$scope.regChkTrans.descripcion = reg[0].descripcion;
				$scope.regChkTrans.estatus = reg[0].estatus;
				$scope.regChkTrans.monto = reg[0].monto;

				$scope.nwRegistro();

			}

			$scope.cancelarReg = function($event){
				$event.preventDefault();
				$scope.regChkTrans = {};
				$scope.NwChkTran = false;
				$scope.LschkTransito = true;
				$scope.geChkTransitoList();
			};

			$scope.setChkTranito = function($event){
				$event.preventDefault();
				try{
					if($scope.regChkTrans.id === undefined){
						$scope.regChkTrans.id = null;
					}

					var RegFecha = $scope.regChkTrans.fecha.split('/');
	      			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
	      			$scope.regChkTrans.fecha = FechaFormat;

					console.log($scope.regChkTrans);
					conciliacionServices.setChkTransito($scope.regChkTrans).then(function (data){
						var resp = data;
						if (resp == "Ok"){
							notie.alert(1,"Registro almacenado de forma exitosa", 3);
						}else{
							notie.alert(3,"Ocurrio un error al realizar el registro",4);
							console.log(resp);
						}
					});
					
					$scope.cancelarReg($event);
				}
				catch(e){
					notie.alert(3,"Ocurrio un error interno en la aplicacion", 4);
					console.log(e);
				}
		};


		};
	}])

	.controller('repConciliacion', ['$scope','$filter', '$rootScope', 'conciliacionServices','$timeout', '$window', 
		function ($scope, $filter, $rootScope, conciliacionServices, $timeout, $window) {
		$scope.fechaI = null;
		$scope.fechaF = null; 
		$scope.printArea = false;
		$scope.regData = {};

		$scope.getDate = function(){
			var date = new Date();
			var dateI = new Date(date.getFullYear(), date.getMonth(), 1)
			var dateF = new Date(date.getFullYear(), date.getMonth() + 1, 0);

			$scope.fechaI = $filter('date')(dateI,'dd/MM/yyyy');
			$scope.fechaF = $filter('date')(dateF,'dd/MM/yyyy');
		};

		$scope.getData = function(){
			conciliacionServices.getConcRep($scope.fechaI, $scope.fechaF).then(function (data){
				$scope.printArea = true;
				$scope.regData = data;
				$window.print();
			});
		}
		
		
	}])
	
	.controller('DepositosCtrl', ['$scope','$filter', '$rootScope', 'conciliacionServices','$timeout', '$window',  
		function ($scope, $filter, $rootScope, conciliacionServices, $timeout, $window) {
			$scope.depositosLs = [];
			$scope.regDeposito = {};
			$scope.fechai = null;
			$scope.fechaf = null;
			$scope.NwDep = false;
			$scope.LsDepts = true;

			$scope.getDepFecha = function(){
				
				var regFechaI = $scope.fechai.split('/');
				var formt1 = regFechaI[2] + '-' + regFechaI[1] + '-' + regFechaI[0]; 

				var regFechaF = $scope.fechaf.split('/');
				var formt2 = regFechaF[2] + '-' + regFechaF[1] + '-' + regFechaF[0]; 


				conciliacionServices.getDepositoFecha(formt1, regFechaF).then(function (data){
					$scope.depositosLs = data;

				
				});
			};

			$scope.getDepositoList = function(){
				$scope.regDeposito = {};
				conciliacionServices.getDeposito().then(function (data){
					$scope.depositosLs = data;
			});

			$scope.NwDeposito = function($event){
				$scope.NwDep = true;
				$scope.LsDepts = false;
			};

			$scope.editReg = function(id){
				var reg = $scope.depositosLs.filter(function(data){
					return data.id == id;
				})
				console.log(reg[0]);
				$scope.regDeposito.id = reg[0].id;
				$scope.regDeposito.fecha = reg[0].fecha;

				var RegFecha = reg[0].fecha.split('-');
	      		var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
	      		$scope.regDeposito.fecha= FechaFormat;

				$scope.regDeposito.descripcion = reg[0].descripcion;
				$scope.regDeposito.estatus = reg[0].estatus;
				$scope.regDeposito.monto = reg[0].monto;

				$scope.NwDeposito();

			}

			$scope.cancelarReg = function($event){
				$event.preventDefault();
				$scope.regDeposito = {};
				$scope.NwDep = false;
				$scope.LsDepts = true;
				$scope.getDepositoList();
			};

			
			$scope.impDeposito = function($event){
				$event.preventDefault();
				$scope.datosR = null;
				$scope.datosT = null;
				$scope.datosC = null;

				$scope.cabeceraR = {tipo: 'Deposito',
									titulo: 'registrado'};

				$scope.cabeceraT = {tipo: 'Deposito',
									titulo: 'en Transito'};

				$scope.cabeceraC = {tipo: 'Deposito',
									titulo: 'Cerrado'};

				$scope.datosR = $scope.depositosLs.filter(function (data){
					return data.estatus == 'R'
					});

				$scope.datosT = $scope.depositosLs.filter(function (data){
					return data.estatus == 'T'
					});

				$scope.datosC = $scope.depositosLs.filter(function (data){
					return  data.estatus == 'C'
					});

				$scope.imprimirReporte($scope.datosR, $scope.cabeceraR);
				$scope.imprimirReporte($scope.datosT, $scope.cabeceraT);
				$scope.imprimirReporte($scope.datosC, $scope.cabeceraC);


			}

			$scope.imprimirReporte = function(datos, cabecera){
				if (datos.length > 0){
					$window.sessionStorage['concCabecera'] = JSON.stringify(cabecera);
					$window.sessionStorage['concGenerico'] = JSON.stringify(datos);
					$window.open('/conciliacion/salida', target='_blank'); 
				}
			};

			$scope.setDeposito = function($event){
				$event.preventDefault();
				try{
					if($scope.regDeposito.id === undefined){
						$scope.regDeposito.id = null;
					}

					var RegFecha = $scope.regDeposito.fecha.split('/');
	      			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
	      			$scope.regDeposito.fecha = FechaFormat;

					console.log($scope.regDeposito);
					conciliacionServices.setDeposito($scope.regDeposito).then(function (data){
						var resp = data;
						if (resp == "Ok"){
							notie.alert(1,"Registro almacenado de forma exitosa", 3);
						}else{
							notie.alert(3,"Ocurrio un error al realizar el registro",4);
							console.log(resp);
						}
					});
					
					$scope.cancelarReg($event);
				}
				catch(e){
					notie.alert(3,"Ocurrio un error interno en la aplicacion", 4);
					console.log(e);
				}
		};
		};
	}])

	.controller('reporteGController', ['$scope', '$filter','$window', function($scope, $filter, $window){
		$scope.datos = JSON.parse($window.sessionStorage['concGenerico']);
		$scope.cabecera = JSON.parse($window.sessionStorage['concCabecera']);
		$scope.total = 0;

		$scope.resultado = function(){
			
			for (var dat in $scope.datos){
				$scope.total += parseInt($scope.datos[dat].monto);
			}
		}
	}]);
	
})();