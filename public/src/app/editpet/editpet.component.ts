import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router, ActivatedRoute } from '@angular/router'; //Add ActivatedRoute for activated routes

@Component({
  selector: 'app-editpet',
  templateUrl: './editpet.component.html',
  styleUrls: ['./editpet.component.css']
})
export class EditpetComponent implements OnInit {
    pet:any;
    skill1: String;
    skill2: String;
    skill3: String;
    skarr: any = [];
    errors: any;

    constructor(
        private _httpService: HttpService,
        private _router: Router,
        private _route: ActivatedRoute
    ){}

    ngOnInit() {
        this.pet = {name: "", type: "", description: "", skills: []};
        this.skill1 = "";
        this.skill2 = "";
        this.skill3 = "";
        this.errors = [];
        this._route.params.subscribe(params=> {
            console.log("Params", params);
            this._httpService.getOne(params['id']).subscribe(data => {
                this.pet = data;
                if(this.pet.skills[0] != undefined) this.skill1 = this.pet.skills[0];
                if(this.pet.skills[1] != undefined) this.skill2 = this.pet.skills[1];
                if(this.pet.skills[2] != undefined) this.skill3 = this.pet.skills[2];
            })
        })
    }

    editPet(){
        console.log("SKILLS: ", this.pet.skills)
        console.log(this.skill1, this.skill2, this.skill3)
        if(this.skill1) this.skarr.push(this.skill1);
        if(this.skill2) this.skarr.push(this.skill2);
        if(this.skill3) this.skarr.push(this.skill3);
        this.pet.skills = this.skarr;
        console.log("PET: ", this.pet);
        this._httpService.updateOne(this.pet._id, this.pet).subscribe(data => {
            console.log(data);
            if(data['good']) {
                // this.allpets.push(this.pet);
                this._router.navigate(['/pets/'+this.pet._id]);
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
        this._router.navigate(['/pets/'+this.pet._id]);
    }

}
