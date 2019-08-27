import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HttpService } from './http.service';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MoviesComponent } from './movies/movies.component';
import { NewComponent } from './new/new.component';
import { ReviewComponent } from './review/review.component';
import { ShowComponent } from './show/show.component';

@NgModule({
  declarations: [
    AppComponent,
    MoviesComponent,
    NewComponent,
    ReviewComponent,
    ShowComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [HttpService],
  bootstrap: [AppComponent]
})
export class AppModule { }
