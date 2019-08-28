import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HttpService } from './http.service';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ShelterComponent } from './shelter/shelter.component';
import { NewpetComponent } from './newpet/newpet.component';
import { PetComponent } from './pet/pet.component';
import { EditpetComponent } from './editpet/editpet.component';

@NgModule({
  declarations: [
    AppComponent,
    ShelterComponent,
    NewpetComponent,
    PetComponent,
    EditpetComponent
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
