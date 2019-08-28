import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router, ActivatedRoute } from '@angular/router'; //Add ActivatedRoute for activated routes

@Component({
  selector: 'app-pet',
  templateUrl: './pet.component.html',
  styleUrls: ['./pet.component.css']
})
export class PetComponent implements OnInit {
    pet:any;
    clicked: boolean;

    constructor(
        private _httpService: HttpService,
        private _router: Router,
        private _route: ActivatedRoute
    ){}

    ngOnInit() {
        this.clicked = false;
        this.pet = {name: "", type: "", description: "", skills: []};
        this._route.params.subscribe(params=> {
            console.log("Params", params);
            this._httpService.getOne(params['id']).subscribe(data => {
                this.pet = data;
                console.log(this.pet)
            })
        })
    }

    like(){
        this.pet['likes']++;
        this._httpService.updateOne(this.pet._id, this.pet).subscribe(data =>{
            if(data['good']) {
                this.clicked = true;
            }
            else {
                this.pet['likes']--;
                alert('Error trying to like pet');
            }
        })
    }

    adopt(){
        this._httpService.deleteOne(this.pet._id).subscribe(data =>{
            console.log(data)});
        this._router.navigate(['/pets'])
    }

}
