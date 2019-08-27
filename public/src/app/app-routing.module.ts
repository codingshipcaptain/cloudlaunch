import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MoviesComponent } from './movies/movies.component';
import { ShowComponent } from './show/show.component';
import { ReviewComponent } from './review/review.component';


const routes: Routes = [
    {path: 'movies', component: MoviesComponent},
    {path: 'movies/:id', component: ShowComponent},
    {path: 'movies/:id/review', component: ReviewComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
