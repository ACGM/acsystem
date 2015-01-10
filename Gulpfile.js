var gulp = require('gulp'),
	connect =require('gulp-connect'),
	jshint= require('gulp-jshint'),
	stylish= require('jshint-stylish'),
	uglify= require('gulp-uglify'),
	gulpif= require('gulp-if'),
	minify= require('gulp-minify-css'),
	useref= require('gulp-useref'),
	concant= require('gulp-concat'),
	nib= require('nib'),
	stylus=require('stylus'),
	templateCache= require('gulp-angular-templatecache'),
	historyApiFallback = require('connect-history-api-fallback');

//Servidor web para gulp
gulp.task('server',function(){
	connect.server({
		root: './ahorro',
		host: '0.0.0.0',
		port: 8080,
		livereload: true,
		middleweare:function(connect, opt){
			return [historyApiFallback];
		}
		});

	});

//tarea para manejar la cache de los template de angular
gulp.task('templatesAhorro',function(){
	gulp.src('./ahorro/templates/*.html')
	.pipe(templateCache({
		root:'templates',
		module: 'cooperativa.Ahorro',
		standalone:true
	}))
	.pipe(gulp.dest('./ahorro/static/js'));
});
//tarea uglifucadora para JS
gulp.task('jsAhorro',function(){
	gulp.src('./ahorro/static/js/libs')
		.pipe(gulpif('*.js',uglify({mangle:false})))
		.pipe(gulp.dest('./ahorro/static/js'));
});

//tarea de Stylus para css
gulp.task('css', function(){
	gulp.src('./acgm/static/stylus/estilos.styl')
		.pipe(stylus({ use:nib() }))
		.pipe(gulp.dest('./acgm/static/css'))
		.pipe(connect.reload());
	});

//Recarga el servidor web cuando haya cambios en el HTML.
gulp.task('htmlAhorro',function(){
	gulp.src('./ahorro/templates/*.html')
		.pipe(connect.reload());
	});

//busca errores en el JavaScript y "Los muestra en pantalla ", ay que probarlo jajajaja
gulp.task('jshintAhorro',function(){
	return gulp.src('./ahorro/static/js/libs/*.js')
			.pipe(jshint())
			.pipe(jshint.reporter('jshint-stylish'))
			.pipe(jshint.reporter('fail'));
	});

//Lanza las tareas cuando detecta cambios
gulp.task('watch', function(){

	gulp.watch(['./ahorro/static/js/libs/*.js'],['jsAhorro']);

	//proceso de watch para css
	gulp.watch(['./acgm/static/stylus/*.styl'],['css']);

	//Proceso de watch para ahorro
	gulp.watch(['./ahorro/templates/*.html'],['htmlAhorro']);

	//Proceso de watch para jshint
	gulp.watch(['./ahorro/static/js/libs/*.js','./Gulpfile.js'],['jshintAhorro']);

	});

//lanza la tarea por defaul, correr el servidor y las tareas de watch
gulp.task('default',['server','watch']);
