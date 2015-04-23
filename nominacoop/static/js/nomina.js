(function (_) {

  angular.module('cooperativa.nomina', ['ngAnimate'])
    
    .factory('NominaService', ['$http', '$q', '$filter', function ($http, $q, $filter) {

      // Retornar las nominas generadas
      function nominasGeneradas() {
        var deferred = $q.defer();

        $http.get('/api/nominasgeneradas/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }

      // Retornar detalle de nomina generada
      function detalleNomina(fecha) {
        var deferred = $q.defer();
        if(fecha != undefined) {
          url = '/api/nomina/detalle/fecha/?format=json'.replace('fecha',fecha);
        } else {
          url = '/api/nomina/detalle/?format=json';
        }

        $http.get(url)
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }

      function detalleEmpleado(nomina,empleado) {
        var deferred = $q.defer();
        detalleNomina(nomina).then(function (data) {
          var result = data.filter(function (emp) {
            return emp.id == empleado.id;
          });

          if(result.length > 0) {
            deferred.resolve(result);
          } else {
            deferred.reject();
          }
        });

        return deferred.promise;
      }

      // Retornar los tipos de nominas
      function tiposNominas() {
        var deferred = $q.defer();

        $http.get('/api/tiposnomina/?format=json')
          .success(function (data) {
            deferred.resolve(data);
          });

          return deferred.promise;
      }


      //Generar nomina (parametros: Fecha y Tipo de Nomina [y Nota])
      function generaNomina(fecha, tipo, quincena, nota) {
        var deferred = $q.defer();

        $http.post('/nomina/generar/', JSON.stringify({'fechaNomina': fecha, 'tipoNomina': tipo, 'quincena': quincena, 'nota': nota})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Aplicar prestamos (registrar descuento del balance MaestraPrestamo)
      function AplicarPrestamos(nomina, tipoPrestamo) {
        var deferred = $q.defer();

        var fecha = nomina.split('/');
        var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

        $http.post('/nomina/descuentos/aplicar/prestamos/', JSON.stringify({'nomina': fechaFormatted, 'tipoPrestamo': tipoPrestamo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Aplicar ahorros (registrar suma de cuota de ahorro)
      function AplicarAhorros(nomina) {
        var deferred = $q.defer();

        var fecha = nomina.split('/');
        var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

        $http.post('/nomina/descuentos/aplicar/ahorros/', JSON.stringify({'nomina': fechaFormatted})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }
      
      //Eliminar nomina (parametros: Fecha y Tipo de Nomina)
      function eliminarNomina(fecha, tipo) {
        var deferred = $q.defer();

        $http.post('/nomina/eliminar/', JSON.stringify({'fechaNomina': fecha, 'tipoNomina': tipo})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;

      }

      //Guardar Cambios en Detalle Nomina para Empleado
      function guardarDetalleEmpleado(nomina, tipoNomina, detalle) {
        var deferred = $q.defer();

        $http.post('/nomina/guardarDE/', JSON.stringify({'nomina': nomina, 'tipoNomina': tipoNomina, 'detalle': detalle})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });

        return deferred.promise;
      }

      //Consultar existencia de Nomina
      function getNomina(fechaNomina, tipoPrestamo) {
        var deferred = $q.defer();

        $http.get('/nomina/verificarExistencia/?nomina={nomina}&tipoPrestamo={tipoPrestamo}'.replace('{nomina}', fechaNomina).replace('{tipoPrestamo}', tipoPrestamo)).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Generar Archivo de Nomina para Prestamos
      function generarArchivoPrestamos(prestamos, fechaNomina, tipoPN) {
        var deferred = $q.defer();

        $http.post('/nomina/archivos/prestamos/', JSON.stringify({'prestamos': prestamos, 'fechaNomina': fechaNomina, 'infoTipo': tipoPN})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Generar Archivo de Nomina para Ahorros
      function generarArchivoAhorros(ahorros, fechaNomina) {
        var deferred = $q.defer();

        $http.post('/nomina/archivos/ahorros/', JSON.stringify({'ahorros': ahorros, 'fechaNomina': fechaNomina})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      //Generar Archivo de Nomina para Balance de Prestamos
      function generarArchivoPrestamosBalance(infoTipo, fechaNomina) {
        var deferred = $q.defer();

        $http.post('/nomina/archivos/prestamos/balance/', JSON.stringify({'infoTipo': infoTipo, 'fechaNomina': fechaNomina})).
          success(function (data) {
            deferred.resolve(data);
          }).
          error(function (data) {
            deferred.resolve(data);
          });
        return deferred.promise;
      }

      return {
        nominasGeneradas        : nominasGeneradas,
        generaNomina            : generaNomina,
        tiposNominas            : tiposNominas,
        detalleNomina           : detalleNomina,
        detalleEmpleado         : detalleEmpleado,
        eliminarNomina          : eliminarNomina,
        guardarDetalleEmpleado  : guardarDetalleEmpleado,
        getNomina               : getNomina,
        generarArchivoPrestamos : generarArchivoPrestamos,
        generarArchivoAhorros   : generarArchivoAhorros,
        AplicarPrestamos        : AplicarPrestamos,
        AplicarAhorros          : AplicarAhorros,
        generarArchivoPrestamosBalance : generarArchivoPrestamosBalance
      };

    }])

    //****************************************************
    //                                                   *
    //CONTROLLERS                                        *
    //                                                   *
    //****************************************************
    .controller('NominaCtrl', ['$scope', '$filter', 'NominaService', function ($scope, $filter, NominaService) {
      $scope.showGN = true;
      $scope.showCN = true;

      $scope.nominaH = {};
      $scope.reg = [];
      $scope.empleado = {};
      $scope.detalle = [];

      //Limpiar variables
      $scope.clearDetalle = function() {
        $scope.reg = [];
        $scope.empleado = {};
        $scope.detalle = [];
        $scope.nomina = '';
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

       // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }

      // Mostrar/Ocultar panel de Consultar Nomina
      $scope.toggleCN = function() {
        $scope.showCN = !$scope.showCN;
      }

      // Mostrar/Ocultar panel de Generar Nomina
      $scope.toggleGN = function() {
        $scope.showGN = !$scope.showGN;
      }

      //Generar la nomina
      $scope.generarNomina = function() {
        try {
          if ($scope.FormGeneraNomina.$valid) {
            var fecha = $scope.nominaH.fechaNomina.split('/');
            var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

            var tipo = $scope.nominaH.tipoNomina;
            var nota = $scope.nominaH.nota != undefined? $scope.nominaH.nota : '';
            var quincena;

            if(parseInt(fecha[0]) > 15) {
              quincena = 2;
            } else {
              quincena = 1;
            }

            NominaService.generaNomina(fechaFormatted,tipo,quincena,nota).then(function (data) {
              console.log(data);
              if(data == -1) {
                $scope.mostrarError("Existe una nomina generada en la fecha que ha seleccionado.");
                throw data;
              }
              if(isNaN(data)) {
                $scope.mostrarError(data);
                throw data;
              }
              $scope.getNominasGeneradas();
              $scope.clearDetalle();
              $scope.errorShow = false;
            },
            function () {
              $scope.mostrarError('Ocurrio un error inesperado, contacte al administrador del sistema' + data);
              throw data;
            });

          } else {
            throw "Verifique que ha completado toda la información requerida.";
          }
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Todos los tipos de Nominas
      $scope.tiposNominas = function() {
        NominaService.tiposNominas().then(function (data) {
          $scope.tiposN = data;
        });
      }

      // Todas las nominas generadas
      $scope.getNominasGeneradas = function() {
        NominaService.nominasGeneradas().then(function (data) {
          $scope.nominas = data;
        });
      }

      //Eliminar Nomina
      $scope.eliminarNominaSel = function(fecha, tipo) {
        NominaService.eliminarNomina(fecha, tipo).then(function (data) {

          $scope.getNominasGeneradas();
          $scope.clearDetalle();
        });
      }

      // Retorna el detalle de una nomina
      $scope.getDetalleNomina = function(nomina, tipoNomina) {
        $scope.nomina = nomina;
        $scope.tipoNomina = tipoNomina;

        NominaService.detalleNomina(nomina).then(function (data) {
          $scope.detalle = data;

          data.forEach(function (data) {
            $scope.reg[data.id] = '';
          });

        });
      }

      // Seleccionar un empleado para ver detalle
      $scope.selEmpleado = function(nomina, empleado) {

        $scope.reg.forEach(function (data, index) {
          $scope.reg[index] = '';
        });
        $scope.reg[empleado.id] = 'empleado-sel';

        NominaService.detalleEmpleado(nomina, empleado).then(function (data) {
          $scope.empleado.salario = $filter('number')(data[0].salario,2);
          $scope.empleado.ars = $filter('number')(data[0].ars,2);
          $scope.empleado.vacaciones = $filter('number')(data[0].vacaciones,2);
          $scope.empleado.afp = $filter('number')(data[0].afp,2);
          $scope.empleado.otrosIngresos = $filter('number')(data[0].otrosIngresos,2);
          $scope.empleado.isr = $filter('number')(data[0].isr,2);
          $scope.empleado.descPrestamos = $filter('number')(data[0].descPrestamos,2);
          $scope.empleado.descAhorros = $filter('number')(data[0].descAhorros,2);
          $scope.empleado.cafeteria = $filter('number')(data[0].cafeteria,2);
          $scope.empleado.horasExtras = $filter('number')(data[0].horasExtras,2);

          $scope.empleado.codigo = data[0]['getcodigo'];
          $scope.empleado.empleado = data[0]['empleado'];

        });
      }

      //Guardar cambios en detalle de empleado.
      $scope.guardarDE = function() {
        try {
          NominaService.guardarDetalleEmpleado($scope.nomina, $scope.tipoNomina, $scope.empleado).then(function (data) {

            console.log('Fueron guardados los cambios con exito.');

            var empleado = _.findWhere($scope.detalle, {getcodigo: $scope.empleado.codigo});

            $scope.getNominasGeneradas();
            $scope.getDetalleNomina($scope.nomina, $scope.tipoNomina);
            $scope.selEmpleado($scope.nomina, empleado);
        
          });
        } catch (e) {
          $scope.mostrarError(e);
        }

      }

    }])

    //****************************************************
    //                                                   *
    //CONTROLLERS --DESCUENTOS PRESTAMOS/AHORROS         *
    //                                                   *
    //****************************************************
    .controller('NominaDescuentosCtrl', ['$scope', '$filter', '$window', 'appService', 'MaestraPrestamoService', 'FacturacionService', 'NominaService', 
                                          function ($scope, $filter, $window, appService, MaestraPrestamoService, FacturacionService, NominaService) {
      $scope.showAHORROS = true;
      $scope.encogeAhorros = 'encogeAhorros';
      $scope.extiendePrestamos = 'extiende';
      $scope.showPRESTAMOS = true;

      $scope.nominaH = {};
      $scope.reg = [];
      $scope.empleado = {};
      $scope.detalle = [];

      $scope.tipoPrestamoNomina = 'RE';

      window.onresize = function(event) {
        panelesSize();
      }

      function panelesSize() {
        document.getElementById('panelPrestamos').style.height = (window.innerHeight - 280) + 'px';
        document.getElementById('panelAhorros').style.height = (window.innerHeight - 280) + 'px';
      }

      // Mostrar/Ocultar error
      $scope.toggleError = function() {
        $scope.errorShow = !$scope.errorShow;
      }

      // Funcion para mostrar error por pantalla
      $scope.mostrarError = function(error) {
        $scope.errorMsg = error;
        $scope.errorShow = true;
      }

      // Mostrar/Ocultar posteo Contabilidad
      $scope.toggleInfo = function() {
        $scope.showPostear = !$scope.showPostear;
      }

      // Traer listado de prestamos de la Maestra que estan activos.
      $scope.listadoPrestamos = function($event, tipoPrestamoNom) {
        $event.preventDefault();

        panelesSize();
        $scope.mensaje = '';

        $scope.prestamos = [];

        try {
          $scope.verificarExistenciaNomina();

          if($scope.fechaNomina == undefined) {
            throw "Verifique que la fecha de nomina no tiene errores."
          }

          MaestraPrestamoService.PrestamosPosteados(tipoPrestamoNom).then(function (data) {
            var fecha = $scope.fechaNomina.split('/');
            var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

            var prestamo;
            
            data.forEach(function (item) {
              prestamo = {};
              prestamo.codigoSocio = item.codigoSocio;
              prestamo.socio = item.socio;
              prestamo.noPrestamo = item.noPrestamo;
              prestamo.montoCuotaQ = fecha[0] > 15? item.montoCuotaQ2 : item.montoCuotaQ1;
              prestamo.cuotaInteresQ = fecha[0] > 15? item.cuotaInteresQ2 : item.cuotaInteresQ1;
              prestamo.cuotaMasInteresQ = fecha[0] > 15? item.cuotaMasInteresQ2 : item.cuotaMasInteresQ1;
              prestamo.balance = $filter('number')(item.balance, 2);

              if(parseFloat(prestamo.montoCuotaQ) > 0 && item.tipoPrestamoNomina == tipoPrestamoNom) {
                $scope.prestamos.push(prestamo);
              }
              $scope.totalesPrestamos();
            });

            $scope.listadoAhorros();
            $scope.errorShow = false;
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      // Trae el listado de ahorros de todos los socios activos.
      $scope.listadoAhorros = function() {
        $scope.ahorros = [];

        FacturacionService.socios().then(function (data) {
          var fecha = $scope.fechaNomina.split('/');
          var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

          var ahorro;
          
          data.forEach(function (item) {
            ahorro = {};
            ahorro.codigo = item.codigo;
            ahorro.nombreCompleto = item.nombreCompleto;
            ahorro.cuotaAhorro = fecha[0] > 15? item.cuotaAhorroQ2 : item.cuotaAhorroQ1;

            if(parseFloat(ahorro.cuotaAhorro) > 0) {
              $scope.ahorros.push(ahorro);
            }
            $scope.totalAhorros();
          });
        });
      }

      // Calcula totales para prestamos regulares.
      $scope.totalesPrestamos = function() {
        $scope.prestamoTotalMontoCuota = 0;
        $scope.prestamoTotalCuotaInteres = 0;
        $scope.prestamoTotalCuotaMasInteres = 0;

        $scope.prestamos.forEach(function (prestamo) {
          $scope.prestamoTotalMontoCuota += parseFloat(prestamo.montoCuotaQ);
          $scope.prestamoTotalCuotaInteres += parseFloat(prestamo.cuotaInteresQ);
          $scope.prestamoTotalCuotaMasInteres += parseFloat(prestamo.cuotaMasInteresQ);
        });
      }

      // Calcula totales para ahorros.
      $scope.totalAhorros = function() {
        $scope.ahorroTotalCuotaAhorro = 0;

        $scope.ahorros.forEach(function (ahorro) {
          $scope.ahorroTotalCuotaAhorro += parseFloat(ahorro.cuotaAhorro);
        });
      }

      // Quitar un prestamo del listado.
      $scope.quitarPrestamo = function(item) {
        $scope.prestamos = _.without($scope.prestamos, _.findWhere($scope.prestamos, {noPrestamo: item.noPrestamo}));
        $scope.totalesPrestamos();
      }

      // Ocultar panel de ahorros.
      $scope.ocultarAhorros = function($event) {
        $event.preventDefault();

        $scope.extiendePrestamos = 'extiende';
        $scope.encogePrestamos = '';
        $scope.encogeAhorros = 'encogeAhorros';
      }

      // Ocultar panel de prestamos.
      $scope.ocultarPrestamos = function($event) {
        $event.preventDefault();

        $scope.extiendeAhorros = 'extiende';
        $scope.encogeAhorros = '';
        $scope.encogePrestamos = 'encogePrestamos';
      }

      // Verificar si existe nomina.
      $scope.verificarExistenciaNomina = function() {
        var fecha = $scope.fechaNomina.split('/');
        var fechaFormatted = fecha[2] + '-' + fecha[1] + '-' + fecha[0];

        var msgAhorro = '';
        var msgPrestamo = '';

        NominaService.getNomina(fechaFormatted, $scope.tipoPrestamoNomina).then(function (data) {
          if(data.length > 0) {
            if(data[0]['ahorros'] == 1) {
              msgAhorro = 'Ahorros generados.';
            }
            if(data[0]['prestamos'] == 1) {
              msgPrestamo = 'Prestamos generados.';
            }
            if(data[0]['ahorros'] == 1 || data[0]['prestamos'] == 1) {
              $scope.mensaje = 'Existe ' + msgPrestamo + ' ' + msgAhorro;
            }
          }
        });
      }

      // Generar Archivo para Prestamos (envio para nomina empleados)
      $scope.archivoPrestamos = function() {

        var fecha = $scope.fechaNomina.split('/');
        var fechaFormatted = fecha[2] + fecha[1] + fecha[0];
        var INFOTIPO;

        switch($scope.tipoPrestamoNomina) {
          case 'RE': INFOTIPO = '0015'; break;
          case 'VA': INFOTIPO = '2010'; break;
          case 'BO': INFOTIPO = '2012'; break;
          case 'RG': INFOTIPO = '2008'; break;
          case 'RI': INFOTIPO = '2012'; break;
        }

        NominaService.generarArchivoPrestamos($scope.prestamos, fechaFormatted, INFOTIPO).then(function (data) {
          if(data != 1) {
            $scope.mostrarError(data);
          } else {
            $scope.mensaje = 'Fue generado el archivo de Prestamos.';
            $scope.errorShow = false;
            alert('El archivo fue generado!');
          }
        });
      }

      // Generar Archivo para Ahorros (envio para nomina empleados)
      $scope.generarArchivoAhorros = function() {

        var fecha = $scope.fechaNomina.split('/');
        var fechaFormatted = fecha[2] + fecha[1] + fecha[0];

        NominaService.generarArchivoAhorros($scope.ahorros,fechaFormatted).then(function (data) {
          console.log(data)

          if(data != 1) {
            $scope.mostrarError(data);
          } else {
            $scope.mensaje = 'Fue generado el archivo de Ahorros.';
            alert('Archivo de ahorros generado!');
          }
        });
      }

      // Para visualizar los archivos de prestamos generados.
      $scope.verArchivo = function(tipoArchivo) {
        var archivo = '';

        switch(tipoArchivo) {
          case 'RE': archivo = 'PA0015.TXT'; break;
          case 'VA': archivo = 'PA2010.TXT'; break;
          case 'BO': archivo = 'PA2012.TXT'; break;
          case 'RG': archivo = 'PA2008.TXT'; break;
          case 'RI': archivo = 'PA2012.TXT'; break;
          case 'AH': archivo = 'PA0014.TXT'; break;

        }
        $window.open('/static/media/{archivo}'.replace('{archivo}', archivo), target='_blank'); 

      }

      // Agregar una cuenta
      $scope.addCuentaContable = function($event, cuenta) {
        $event.preventDefault();
        var desgloseCuenta = new Object();

        desgloseCuenta.cuenta = cuenta.codigo;
        desgloseCuenta.descripcion = cuenta.descripcion;
        desgloseCuenta.ref = $scope.desgloseCuentas[$scope.desgloseCuentas.length-1].ref;
        desgloseCuenta.debito = 0;
        desgloseCuenta.credito = 0;

        $scope.desgloseCuentas.push(desgloseCuenta);
        $scope.tableCuenta = false;
      }

      $scope.quitarCC = function(desgloseC) {
        if($scope.desgloseCuentas.length == 1) {
          $scope.mostrarError("No puede eliminar todas las cuentas. Verifique la configuración de Documentos-Cuentas.")
        } else {
          $scope.desgloseCuentas = _.without($scope.desgloseCuentas, _.findWhere($scope.desgloseCuentas, {cuenta: desgloseC.cuenta}));
        }
      }

      //Funcion para aplicar prestamos (realizar descuentos del monto de balance de la mestra de Prestamos)
      $scope.aplicarPrestamos = function() {
        try {
          NominaService.AplicarPrestamos($scope.fechaNomina, $scope.tipoPrestamoNomina).then(function (data) {
            if(data == 1) {
              alert('Fueron aplicados los prestamos con exito!');
              $scope.errorShow = false;
            } else {
              $scope.mostrarError(data);
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Funcion para aplicar ahorros (realizar deposito al ahorro del socio)
      $scope.aplicarAhorros = function() {
        try {
          NominaService.AplicarAhorros($scope.fechaNomina).then(function (data) {
            if(data == 1) {
              alert('Fueron aplicados los ahorros con exito!');
              $scope.errorShow = false;
            } else {
              $scope.mostrarError(data);
            }
          });
        } catch (e) {
          $scope.mostrarError(e);
        }
      }

      //Generar archivo de Balances de Prestamos
      $scope.archivoBalancePrestamos = function($event) {
        $event.preventDefault();

        var fecha = $scope.fechaNomina.split('/');
        var fechaFormatted = fecha[2] + fecha[1] + fecha[0];

        NominaService.generarArchivoPrestamosBalance('9999', fechaFormatted).then(function (data) {
          console.log(data)

          if(data != 1) {
            $scope.mostrarError(data);
          } else {
            $scope.mensaje = 'Fue generado el archivo de Balance de Prestamos.';
            alert('Archivo de balances de prestamos fue generado!');
          }
        });
      }

      //
      $scope.verBalancesPrestamos = function($event) {
        $event.preventDefault();

        $window.open('/static/media/{archivo}'.replace('{archivo}', 'PA9999.TXT'), target='_blank'); 
      }

      //Funcion para postear los registros seleccionados. (Postear es llevar al Diario)
      $scope.postearPrestamos = function() {
        var idoc = 0;
        $scope.iDocumentos = 0;
        $scope.totalDebito = 0.00;
        $scope.totalCredito = 0.00;

        $scope.showPostear = true;
        $scope.desgloseCuentas = [];

        appService.getDocumentoCuentas('NOMP').then(function (data) {
          $scope.documentoCuentas = data;
  
          //Prepara cada linea de posteo
          $scope.documentoCuentas.forEach(function (documento) {
            var desgloseCuenta = new Object();

            if (documento.accion == 'D') {
              if (documento.accion == 'D') {

              }
              $scope.totalDebito += parseFloat($scope.prestamoTotalMontoCuota.toString().replace('$','').replace(',',''));
            } else {
              $scope.totalCredito += parseFloat($scope.prestamoTotalCuotaMasInteres.toString().replace('$','').replace(',',''));
            }

            desgloseCuenta.cuenta = documento.getCuentaCodigo;
            desgloseCuenta.descripcion = documento.getCuentaDescrp;
            desgloseCuenta.ref = documento.getCodigo + $scope.fechaNomina.replace('/','');
            desgloseCuenta.debito = documento.accion == 'D'? $scope.prestamoTotalMontoCuota.toString().replace('$','') : $filter('number')(0.00, 2);
            desgloseCuenta.credito = documento.accion == 'C'? $scope.prestamoTotalMontoCuota.toString().replace('$','') : $filter('number')(0.00, 2);

            $scope.desgloseCuentas.push(desgloseCuenta);
          });
        });
      }

    }]);

})(_);