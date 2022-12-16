<template>
  <div class="container2">
<div  class="inner-container2">
  <div class="titlee"><h1 class="text-center fw-bold mt-6 text-pink">Example</h1></div>

    <b-table style="background-color: #FFFFFF; width: 100%; font-size: 15px !important;"  bordered hover small :items="items" head-variant="dark">
     <template #cell(Check_report)="data">
    <a :href="`#${data.value}`">Go</a>
      </template>

    </b-table>
  <p style="font-size: 20px;">All datasets shown in Example can be downloaded via the SRA accession.</p>
  <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
  </div>
</div>
</template>

<script>



export default {
name: 'Example',
data() {
      return {
        items: [
          { ID: '1', SRA_Accession: 'SRR10971381', Species: 'SCOV2','multistrain':'N','region':'China','Known Clade/Subtype/Strain':'19A',
           'Datasize':'19.4G','Analysis time':'3min','Strain in DB':'Y','Check_report':'/SRR10971381' },
          { ID: '2', SRA_Accession: 'SRR15224359', Species: 'SCOV2','multistrain':'N','region':'USA','Known Clade/Subtype/Strain':'21G (Lambda)',
           'Datasize':'1.9G','Analysis time':'2min','Strain in DB':'N','Check_report':'/SRR15224359' },
          { ID: '3', SRA_Accession: 'SRR961514', Species: 'HIV','multistrain':'Y','region':'NA','Known Clade/Subtype/Strain':'YU2, HXB2, JRCSF, 89.6, NL43',
           'Datasize':'687M','Analysis time':'1min','Strain in DB':'Y','Check_report':'/SRR961514' },
          { ID: '4', SRA_Accession: 'SRR15011445', Species: 'H1N1','multistrain':'N','region':'Karaganda','Known Clade/Subtype/Strain':'1A',
            'Datasize':'297M','Analysis time':'30s','Strain in DB':'N','Check_report':'/SRR15011445' },
          { ID: '5', SRA_Accession: 'ERR3253398', Species: 'HBV','multistrain':'Y','region':'UK','Known Clade/Subtype/Strain':'MK720631,MK720628',
            'Datasize':'15M','Analysis time':'20s','Strain in DB':'Y','Check_report':'/ERR3253398' }
        ]
      }
    }
}
</script>

<style>
.container2 {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  /*height: 100vh;*/
}

.inner-container2 {
  border: 0px solid black;
  width: 70%;
  height: 90%;
  text-align: justify;
  padding-top: 110px;
}
.titlee{
  padding:20px;
}
/*.btable{*/
/*  font-size: 15px;*/
/*}*/
</style>
