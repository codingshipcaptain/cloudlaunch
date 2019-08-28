import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router } from '@angular/router'; //Add ActivatedRoute for activated routes

@Component({
  selector: 'app-newpet',
  templateUrl: './newpet.component.html',
  styleUrls: ['./newpet.component.css']
})
export class NewpetComponent implements OnInit {
    pet: any;
    skill1: String;
    skill2: String;
    skill3: String;
    errors: any;

    constructor(private _httpService: HttpService, private _router: Router){}

    ngOnInit() {
        this.pet = {name: "", type: "", description: "", skills: []};
        this.skill1 = "";
        this.skill2 = "";
        this.skill3 = "";
        this.errors = [];
    }

    addPet() {
        if(this.skill1) this.pet.skills.push(this.skill1);
        if(this.skill2) this.pet.skills.push(this.skill2);
        if(this.skill3) this.pet.skills.push(this.skill3);
        console.log(this.pet)
        this._httpService.createOne(this.pet).subscribe(data => {
            console.log(data);
            if(data['good']) {
                // this.allpets.push(this.pet);
                this._router.navigate(['/pets']);
            }
            else {
                let temp = data['tobj'];
                console.log(temp);
                for(var e = 0; e<temp.length; e++ ){
                    console.log(temp[e]);
                    for(var key in temp[e]){
                        console.log(key);
                        console.log(temp[e][key]);
                        this.errors.push(temp[e][key])
                    }
                }
                console.log(this.errors);
            }
        });

    }

    cancel() {
        this._router.navigate(['/pets']);
    }
}
