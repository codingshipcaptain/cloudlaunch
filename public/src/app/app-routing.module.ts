import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ShelterComponent } from './shelter/shelter.component';
import { NewpetComponent } from './newpet/newpet.component';
import { PetComponent } from './pet/pet.component';
import { EditpetComponent } from './editpet/editpet.component';


const routes: Routes = [
    {path: 'pets', component: ShelterComponent},
    {path: 'pets/new', component: NewpetComponent},
    {path: 'pets/:id', component: PetComponent},
    {path: 'pets/:id/edit', component: EditpetComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
