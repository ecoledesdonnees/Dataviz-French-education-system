var gulp 	= require('gulp'),
    watch 	= require('gulp-watch'),
    livereload = require('gulp-livereload')

gulp.task('watch',function(){
	livereload.listen();
	gulp.watch('./*.html', ['reload']);
})

gulp.task('reload', function(){
	gulp.src('./*.html')
		.pipe(livereload());
})

gulp.task('default', ['watch','reload']);
