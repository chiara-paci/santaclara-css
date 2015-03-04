from django.db import models
from django.core import validators
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

class CssColor(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    hexadecimal=models.CharField(max_length=6,blank=True,
                                 validators=[validators.MinLengthValidator(6),
                                             validators.RegexValidator(regex=r'^[0-9abcdefABCDEF]+$')])
    red = models.PositiveIntegerField(validators=[validators.MinValueValidator(0),
                                                  validators.MaxValueValidator(255)],blank=True)
    green = models.PositiveIntegerField(validators=[validators.MinValueValidator(0),
                                                    validators.MaxValueValidator(255)],blank=True)
    blue = models.PositiveIntegerField(validators=[validators.MinValueValidator(0),
                                                   validators.MaxValueValidator(255)],blank=True)
    
    def save(self,*args,**kwargs):
        if self.id==0:
            self.red=0
            self.green=0
            self.blue=0
            self.hexadecimal=""
            super(CssColor, self).save(*args, **kwargs)
            return
        if not self.red: self.red=0
        if not self.green: self.green=0
        if not self.blue: self.blue=0
        if not self.hexadecimal:
            self.hexadecimal="%2.2x%2.2x%2.2x" % (self.red,self.green,self.blue)
        else:
            r=self.hexadecimal[0:2]
            g=self.hexadecimal[2:4]
            b=self.hexadecimal[4:6]
            self.red=int(r,16)
            self.green=int(g,16)
            self.blue=int(b,16)
        super(CssColor, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.name)

    def rgb(self):
        if self.id==0:
            return u"transparent"
        U= u"%d,%d,%d" % (self.red,self.green,self.blue)
        return U

    class Meta:
        ordering = [ "name" ]

class CssColorVariable(models.Model):
    name = models.SlugField(unique=True)
    color = models.ForeignKey(CssColor)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssColorVariable, self).save(*args, **kwargs)
        key="COLOR_"+unicode(self.name)
        value=unicode(self)
        CssVariable.objects.mk_variable(key,value)

    def __unicode__(self):
        if self.color.id==0:
            return u"transparent"
        U=u"rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % self.color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        return U

class CssShadow(models.Model):
    h_shadow = models.CharField(max_length=1024)
    v_shadow = models.CharField(max_length=1024)
    blur = models.CharField(max_length=1024)
    spread = models.CharField(max_length=1024)

    class Meta:
        unique_together = ("h_shadow","v_shadow","blur","spread")
        ordering = ("h_shadow","v_shadow","blur","spread")

    def __unicode__(self):
        U=self.h_shadow+u" "+self.v_shadow+u" "+self.blur+u" "+self.spread
        return U

    def shadow_text(self):
        U=self.h_shadow+u" "+self.v_shadow+u" "+self.blur
        return U

    def save(self,*args,**kwargs):
        super(CssShadow, self).save(*args, **kwargs)

class CssShadowVariable(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    shadows = models.ManyToManyField(CssShadow,through='CssShadowThrough')
    shadow_text = models.BooleanField(default=False)

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssShadowVariable, self).save(*args, **kwargs)
        key="SHADOW_"+unicode(self.name)
        value=unicode(self)
        CssVariable.objects.mk_variable(key,value)

    def __unicode__(self):
        U=[]
        if self.shadow_text:
            for rel in self.cssshadowthrough_set.all():
                U.append( rel.shadow_text() )
        else:
            for rel in self.cssshadowthrough_set.all():
                U.append( unicode(rel) )
        return u", ".join(U)

class CssShadowThrough(models.Model):
    variable = models.ForeignKey(CssShadowVariable)
    shadow = models.ForeignKey(CssShadow)
    color = models.ForeignKey(CssColor)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)
    inset = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.color.id==0:
            return u"none"
        U=unicode(self.shadow)
        U+=u" rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % self.color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        if self.inset:
            U+=u" inset"
        return U

    def shadow_text(self):
        if self.color.id==0:
            return u"none"
        U=self.shadow.shadow_text()
        U+=u" rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % self.color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        if self.inset:
            U+=u" inset"
        return U

class CssEquivalence(models.Model):
    name = models.CharField(unique=True,max_length=1024)

    def __unicode__(self): return self.name

    class Meta:
        ordering = [ "name" ]

class CssEquivalenceStyle(models.Model):
    name = models.CharField(unique=True,max_length=1024)

    def __unicode__(self): return self.name

    class Meta:
        ordering = [ "name" ]

class CssEquivalenceColor(models.Model):
    equivalence = models.ForeignKey(CssEquivalence)
    style = models.ForeignKey(CssEquivalenceStyle)
    color = models.ForeignKey(CssColor)

    class Meta:
        unique_together = ("equivalence","style")
        ordering = ("equivalence",)
    
    def __unicode__(self): return unicode(self.style)+" "+unicode(self.equivalence)

class CssEquivalenceColorVariable(models.Model):
    name = models.SlugField(unique=True)
    equivalence = models.ForeignKey(CssEquivalence)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)

    class Meta:
        ordering = [ "name" ]

    def __unicode__(self):
        U=unicode(self.name)+": "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        return U

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssEquivalenceColorVariable, self).save(*args, **kwargs)
        name=unicode(self.name)
        for style,color in self.color_dict():
            key="COLOR_"+style.upper()+"_"+name
            value=color
            CssVariable.objects.mk_variable(key,value)

    def color_desc(self,color):
        if color.id==0:
            return u"transparent"
        U=u"rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        return U

    def color_dict(self):
        T={}
        for eq_color in self.equivalence.cssequivalencecolor_set.all():
            style=unicode(eq_color.style)
            T[style]=self.color_desc(eq_color.color)
        return T.items()

    def by_style(self,style):
        eq_color=self.color.equivalence.cssequivalencecolor_set.get(style=style)
        color=self.color.color_desc(eq_color.color)
        return color

class CssEquivalenceShadowVariable(models.Model):
    name = models.CharField(unique=True,max_length=1024)
    shadows = models.ManyToManyField(CssShadow,through='CssEquivalenceShadowThrough')
    shadow_text = models.BooleanField(default=False)

    class Meta:
        ordering = [ "name" ]

    def save(self,*args,**kwargs):
        self.name=self.name.upper()
        super(CssEquivalenceShadowVariable, self).save(*args, **kwargs)
        name=unicode(self.name)
        for style,shadow in self.shadow_dict():
            key="SHADOW_"+style.upper()+"_"+name
            value=shadow
            CssVariable.objects.mk_variable(key,value)

    def __unicode__(self):
        U=[]
        if self.shadow_text:
            for rel in self.cssequivalenceshadowthrough_set.all():
                U.append( rel.shadow_text() )
        else:
            for rel in self.cssequivalenceshadowthrough_set.all():
                U.append( unicode(rel) )
        return unicode(self.name)+u": "+u", ".join(U)

    def shadow_dict(self):
        T={}
        for eq_shadow in self.cssequivalenceshadowthrough_set.all():
            for eq_color in eq_shadow.equivalence.cssequivalencecolor_set.all():
                style=unicode(eq_color.style)
                if not T.has_key(style):
                    T[style]=[]
                T[style].append(eq_shadow.shadow_desc(eq_color.color,self.shadow_text))
        R=[]
        for style,shadow_list in T.items():
            R.append( (style,",".join(shadow_list)) )
        return R

    def by_style(self,style):
        T=[]
        for eq_shadow in self.cssequivalenceshadowthrough_set.all():
            eq_color=eq_shadow.equivalence.cssequivalencecolor_set.get(style=style)
            T.append(eq_shadow.shadow_desc(eq_color.color,self.shadow_text))
        return ",".join(T)

class CssEquivalenceShadowThrough(models.Model):
    variable = models.ForeignKey(CssEquivalenceShadowVariable)
    shadow = models.ForeignKey(CssShadow)
    equivalence = models.ForeignKey(CssEquivalence)
    alpha = models.FloatField(validators=[validators.MinValueValidator(0.0),
                                          validators.MaxValueValidator(1.0)],
                              default=1.0)
    inset = models.BooleanField(default=False)
    

    class Meta:
        ordering = [ "variable" ]

    def save(self,*args,**kwargs):
        super(CssEquivalenceShadowThrough, self).save(*args, **kwargs)
        name=unicode(self.variable.name)
        for style,shadow in self.variable.shadow_dict():
            key="SHADOW_"+style.upper()+"_"+name
            value=shadow
            CssVariable.objects.mk_variable(key,value)

        
    def shadow_desc(self,color,is_shadow_text):
        if is_shadow_text:
            U=self.shadow.shadow_text()
        else:
            U=unicode(self.shadow)
        U+=" "
        if color.id==0:
            U+=u"transparent"
            if self.inset:
                U+=u" inset"
            return U
        U+=u"rgb"
        if self.alpha!=1.0:
            U+=u"a"
        U+= u"(%s" % color.rgb()
        if self.alpha!=1.0:
            U+=u",%2.2f" % self.alpha
        U+=u")"
        if self.inset:
            U+=u" inset"
        return U

    def __unicode__(self):
        U=unicode(self.shadow)+" "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        if self.inset:
            U+=u" inset"
        return U

    def shadow_text(self):
        U=self.shadow.shadow_text()+" "+unicode(self.equivalence)+" (alpha="+("%2.2f" % self.alpha)+")"
        if self.inset:
            U+=u" inset"
        return U

class CssVariableManager(models.Manager):
    def mk_variable(self,key,value):
        var_obj,created=self.get_or_create(key=key,defaults={"value":value})
        if not created:
            var_obj.value=value
            var_obj.save()
        return var_obj,created

class CssVariable(models.Model):
    key = models.CharField(unique=True,max_length=2048)
    value = models.CharField(max_length=2048)
    objects = CssVariableManager()

    def __unicode__(self):
        return unicode(self.key)+u": "+unicode(self.value)

    class Meta:
        ordering = [ "key" ]

###########

class CssEquivalenceBorder(models.Model):
    width = models.CharField(max_length=128,default="1px")
    color = models.ForeignKey(CssEquivalenceColorVariable)
    border_style = models.CharField(max_length=128,default='solid',choices = ( ( "dotted", "dotted" ),
                                                                               ( "dashed", "dashed" ),
                                                                               ( "solid", "solid" ),
                                                                               ( "double", "double" ),
                                                                               ( "groove", "groove" ),
                                                                               ( "ridge", "ridge" ),
                                                                               ( "inset", "inset" ),
                                                                               ( "outset", "outset" ) ) )
    
    def __unicode__(self):
        U=unicode(self.width)+" "+unicode(self.border_style)+" "+unicode(self.color.name)
        return U

    def border_dict(self):
        T=[]
        for style,color in self.color.color_dict():
            T.append( (style,unicode(self.width)+" "+unicode(self.border_style)+" "+color) )
        return T

class CssEquivalenceLinearGradient(models.Model):
    direction =  models.CharField( max_length=128, default="top")
    colors = models.ManyToManyField(CssEquivalenceColorVariable,through='CssEquivalenceLinearGradientThrough')

    def __unicode__(self):
        U=unicode(self.direction)
        for color in self.colors.all():
            U+=u" "+unicode(color.name)
        return U

    def gradient_dict(self):
        T={}
        for rel in self.cssequivalencelineargradientthrough_set.order_by('pos'):
            for style,color in rel.color.color_dict():
                if not T.has_key(style): T[style]='linear-gradient('+unicode(self.direction)
                T[style]+=","+color
        for k in T.keys():
            T[k]+=')'
        return T.items()
        

    # def background_gradient(style,*args):
#     colors=",".join(args);
#     gradient='linear-gradient('+style+','+colors+')'


class CssEquivalenceLinearGradientThrough(models.Model):
    color = models.ForeignKey(CssEquivalenceColorVariable)
    gradient = models.ForeignKey(CssEquivalenceLinearGradient)
    pos = models.PositiveIntegerField()

    class Meta:
        ordering = [ "pos" ]

class CssEquivalenceSection(models.Model):
    name = models.CharField(max_length=1024)

    def __unicode__(self): return unicode(self.name)
    
class CssEquivalenceSelector(models.Model):
    section = models.ForeignKey(CssEquivalenceSection)
    selector = models.CharField(max_length=1024)

    def __unicode__(self): return unicode(self.selector)

class CssEquivalenceStanza(models.Model):
    selectors = models.ManyToManyField(CssEquivalenceSelector)
    box_shadow = models.ManyToManyField(CssEquivalenceShadowVariable,blank=True,through='CssEquivalenceStanzaBoxShadowThrough')
    borders = models.ManyToManyField(CssEquivalenceBorder,blank=True,through='CssEquivalenceStanzaBorderThrough')
    colors = models.ManyToManyField(CssEquivalenceColorVariable,blank=True,through='CssEquivalenceStanzaColorThrough')
    linear_gradients = models.ManyToManyField(CssEquivalenceLinearGradient,blank=True,through='CssEquivalenceStanzaLinearGradientThrough')
    
    def __unicode__(self): 
        U=u""
        sep=u""
        for sel in self.selectors.all():
            U+=sep+unicode(sel)
            sep=u", "
        return U

    def stanza_dict(self):
        T={}
        for eq_style in CssEquivalenceStyle.objects.all():
            T[unicode(eq_style)]=[]
        for rel in self.cssequivalencestanzaboxshadowthrough_set.all():
            box_shadow=rel.shadow
            suffix=""
            if rel.important: suffix=" !important" 
            for style,shadow in rel.shadow.shadow_dict():
                T[style].append( ('box-shadow',shadow+suffix) )
                for i in ["webkit","moz"]:
                    T[style].append( ('-'+i+'-box-shadow',shadow+suffix) )
        for rel in self.cssequivalencestanzacolorthrough_set.all():
            if rel.target=="fore": label="color"
            else: label="background-color"
            suffix=""
            if rel.important: suffix=" !important" 
            for style,color in rel.color.color_dict():
                T[style].append( (label,color+suffix) );
        for rel in self.cssequivalencestanzaborderthrough_set.all():
            suffix=""
            if rel.important: suffix=" !important" 
            label="border-"+unicode(rel.position)
            for style,border in rel.border.border_dict():
                T[style].append( (label,border+suffix) );
        for rel in self.cssequivalencestanzalineargradientthrough_set.all():
            suffix=""
            if rel.important: suffix=" !important" 
            label="background"
            for style,gradient in rel.gradient.gradient_dict():
                T[style].append( (label,gradient+suffix) );
                for i in ["webkit","moz","ms","o"]:
                    T[style].append( (label,'-'+i+'-'+gradient+suffix) )

        return T.items()
            
        

# def background_gradient(style,*args):
#     colors=",".join(args);
#     gradient='linear-gradient('+style+','+colors+')'
#     S='background: '+gradient+';\n'
#     # inverso rispetto agli altri, questo per style=top, cambiare se serve altro
#     #S+='background: -webkit-gradient(linear, 0% 0%, 0% 100%, from('+stop+'), to('+start+'));'
#     for i in ["webkit","moz","ms","o"]:
#         S+='background: -'+i+'-'+gradient+';\n'
#     return S

class CssEquivalenceStanzaBoxShadowThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    shadow = models.ForeignKey(CssEquivalenceShadowVariable)
    important = models.BooleanField(default=False)

    def __unicode__(self): return unicode(self.shadow)

    class Meta:
        unique_together = [ "stanza","shadow" ]

class CssEquivalenceStanzaBorderThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    border = models.ForeignKey(CssEquivalenceBorder)
    important = models.BooleanField(default=False)
    position = models.CharField(max_length=128,choices=( ( "left","left" ),
                                                         ( "top", "top" ),
                                                         ( "right", "right" ),
                                                         ( "bottom", "bottom" ) ) )

    def __unicode__(self): return unicode(self.border)+" ("+unicode(self.position)+")"

    class Meta:
        unique_together = [ "stanza","border","position" ]
    
class CssEquivalenceStanzaColorThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    color = models.ForeignKey(CssEquivalenceColorVariable)
    important = models.BooleanField(default=False)
    target = models.CharField(max_length=128,choices = ( ( "back","back" ),
                                                         ( "fore", "fore" ) ) )

    class Meta:
        unique_together = [ "stanza","color","target" ]

    def __unicode__(self): return unicode(self.color)+" ("+unicode(self.target)+")"

class CssEquivalenceStanzaLinearGradientThrough(models.Model):
    stanza = models.ForeignKey(CssEquivalenceStanza)
    gradient = models.ForeignKey(CssEquivalenceLinearGradient)
    important = models.BooleanField(default=False)
    target = models.CharField(max_length=128,choices = ( ( "back","back" ), ) )

    class Meta:
        unique_together = [ "stanza","gradient","target" ]
    
    def __unicode__(self): return unicode(self.gradient)
