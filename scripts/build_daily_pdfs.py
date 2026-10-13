"""PDF-only presentation of daily quizzes. Requires reportlab and pypdf."""
from pathlib import Path
import json,html,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[1]

def printable(q):
 text=q['question'];answers=list(q['acceptedAnswers']);reason=q['explanation']
 text=re.sub(r'\s*Χρησιμοποίησε [^.]+\.', '', text)
 text=re.sub(r'\s*Γράψε τα δύο κενά χωρισμένα με / \.', '', text)
 text=re.sub(r'\s*Γράψε όλα τα κενά, με τη σειρά, χωρισμένα με / \.', '', text)
 if 'Ανώμαλο ρήμα' in text:
  text=text.replace('πληκτρολόγησε τον αόριστο (Simple Past).','Αόριστος: ___').replace('πληκτρολόγησε τη μετοχή (past participle).','Μετοχή: ___')
 # Both clauses now have unanswered verbs. Answer order follows the printed blanks.
 if 'we arrived' in text:
  if text.startswith('After '):
   text=text.replace('we arrived','we ___ (arrive)');answers=['had finished / arrived','finished / arrived']
   reason='Η ολοκλήρωση προηγείται της άφιξης: had + finished, και arrived για το μεταγενέστερο γεγονός. Είναι επίσης σωστό finished / arrived, επειδή το after δηλώνει ήδη τη σειρά των γεγονότων.'
  elif text.startswith(('By the time','Before')):
   before=text.startswith('Before');text=text.replace('we arrived','we ___ (arrive)');answers=['arrived / '+a for a in answers]
   if before:
    if '(not finish)' in text:answers.extend(['arrived / did not finish','arrived / didn’t finish'])
    else:answers.append('arrived / did / finish')
   reason='Η άφιξη είναι το μεταγενέστερο γεγονός: arrived (Simple Past). Η άλλη πράξη αναφέρεται σε χρόνο πριν από την άφιξη: had + finished, με not στην άρνηση ή had πριν από το υποκείμενο στην ερώτηση.'
   if before:reason+=' Με before είναι επίσης σωστή η χρήση Simple Past και στα δύο μέρη, όπως στις εναλλακτικές λύσεις.'
  elif text.endswith('before we arrived?'):
   text=text.replace('we arrived','we ___ (arrive)');answers=['had / finished / arrived','did / finish / arrived']
   reason='Had + υποκείμενο + finished: ερώτηση για ολοκλήρωση πριν από την άφιξη. Η άφιξη δίνεται με arrived. Επίσης σωστό did / finish / arrived, αφού το before καθορίζει τη χρονική σειρά.'
 # Apply the course rule: specific past time is assessed as Past Continuous only.
 if q.get('tense')=='Past Continuous':
  answers=list(q['acceptedAnswers']);reason=q['explanation']
 reason=reason.replace('με τον ζητούμενο χρόνο, ','').replace('τον ζητούμενο Past Perfect','Past Perfect')
 text=text.replace('___','________________________________')
 return dict(question=text,answers=list(dict.fromkeys(answers)),explanation=reason)

def build():
 out=ROOT/'daily-pdfs';out.mkdir(exist_ok=True)
 # Adjust these paths if running on a system without DejaVu fonts.
 pdfmetrics.registerFont(TTFont('Greek','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
 pdfmetrics.registerFont(TTFont('GreekBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
 s=getSampleStyleSheet()
 for n in ['Normal','Title','Heading2']:s[n].fontName='Greek' if n=='Normal' else 'GreekBold'
 s['Normal'].fontSize=9;s['Normal'].leading=14;s['Normal'].spaceAfter=5
 s['Title'].fontSize=20;s['Title'].leading=25
 s['Heading2'].fontSize=10;s['Heading2'].leading=14;s['Heading2'].spaceBefore=4;s['Heading2'].spaceAfter=3
 p=lambda text,style='Normal':Paragraph(html.escape(text),s[style])
 writer=PdfWriter()
 for day in range(1,31):
  data=json.loads((ROOT/'content'/f'daily-{day:02d}-quiz.json').read_text());qs=[printable(q) for q in data]
  story=[p(f'Ημέρα {day} - Επανάληψη χρόνων','Title'),p('Όνομα: ____________________   Ημερομηνία: ______________'),p('Συμπλήρωσε τα κενά μέσα στις προτάσεις με τον κατάλληλο τύπο των ρημάτων σε παρένθεση. Όπου υπάρχουν δύο προτάσεις, συμπλήρωσε και τα δύο ρήματα.'),Spacer(1,14)]
  for i,q in enumerate(qs,1):story.append(KeepTogether([p(f'{i}. {q["question"]}'),Spacer(1,13)]))
  story.extend([PageBreak(),p(f'Ημέρα {day} - Λύσεις και εξηγήσεις','Title'),p('Στις ασκήσεις με συγκεκριμένη ώρα στο παρελθόν δεχόμαστε μόνο Past Continuous. Σε άλλο πλαίσιο, ο Simple Past θα περιέγραφε ολοκληρωμένο γεγονός εκείνη την ώρα. Εδώ εξασκούμε την πράξη σε εξέλιξη. Άλλες αποδεκτές εναλλακτικές δίνονται με «ή».')])
  for i,q in enumerate(qs,1):story.append(KeepTogether([p(f'{i}. '+ ' ή '.join(q['answers']),'Heading2'),p(q['explanation']),Spacer(1,2)]))
  def footer(canvas,doc):
   canvas.setFont('Greek',8);canvas.drawString(45,25,f'Ημέρα {day} - Επανάληψη χρόνων');canvas.drawRightString(550,25,str(doc.page))
  path=out/f'Day-{day:02d}.pdf';SimpleDocTemplate(str(path),pagesize=(595,842),leftMargin=45,rightMargin=45,topMargin=35,bottomMargin=42,title=f'Ημέρα {day} - 10 ασκήσεις και λύσεις').build(story,onFirstPage=footer,onLaterPages=footer)
  writer.append(PdfReader(str(path)),outline_item=f'Ημέρα {day}')
 writer.add_metadata({'/Title':'Επανάληψη χρόνων - 30 ημέρες με κενά μέσα στις προτάσεις'})
 with (ROOT/'Daily-Tenses-30-Days.pdf').open('wb') as f:writer.write(f)
 print('Updated 30 daily PDFs and combined workbook; quiz JSON unchanged')
if __name__=='__main__':build()
