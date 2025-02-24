let mysql = require('mysql');
let express=require("express")
const app=express();
app.use(express.urlencoded({ extended: false }));
app.use(express.json);

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    port: 3306,
    database: "pfe"
  });
  
  con.connect(function(err) {
    if (err) throw err;
    console.log('db ' + con.state);
  });

app.post("/ajouterutilisateur",(req,res)=>{
    const {nom,prenom,email,mot_de_passe,role}=req.body;
    con.query('SELECT * FROM utilisateurs WHERE email = ?', [email], (err, results) => {
        if (err) {
          return res.status(500).send("utilisateur n'a pas pu etre identifier avant d'étre ajouté");
        }
    
        if (results.length > 0) {

          return res.status(400).send('Utilisateur avec cette email existe deja');
        } else {
    var sql = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (?,?,?,?,?);";
  con.query(sql,[nom,prenom,email,mot_de_passe,role] , function (err, result) {
    if (err) {
        return res.status(500).send("utilisateur n'a pas pu etre ajouter");
      }
    console.log("utilisateur ajouter");
  });
}
    });
});

app.post("/ajouterfuite",(req,res)=>{
    const {information,lien,source,date}=req.body;
    con.query('SELECT * FROM fuite WHERE information = ?', [information], (err, results) => {
        if (err) {
          return res.status(500).send("la fuite n'a pas pu etre identifier avant d'étre ajouté");
        }
    
        if (results.length > 0) {

          return res.status(400).send('information existe deja');
        } else {
    var sql = "INSERT INTO fuite (information,lien,source,date) VALUES (?,?,?,?);";
  con.query(sql,[information,lien,source,date] , function (err, result) {
    if (err) {
        return res.status(500).send("l'information n'a pas pu etre ajouter");
      }
    console.log("information ajouter");
  });
}
    });
});

app.get("/extrairefuite",(req,res)=>{
  id=req.query.id;
  con.query("SELECT * FROM fuite WHERE id= ?;",[id], function (err, result) {
    if (err) {
        return res.status(500).send("la fuite n'a pas pu etre extrait");
      }
    res.json(result[0]);
  });
})
app.listen(3000);